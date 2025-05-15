# receipts_route.py - Fix the username attribute issue

from flask import Blueprint, render_template, request, jsonify, send_file, abort, current_app
from flask_login import login_required, current_user
from datetime import datetime
import io
import base64
import os
from PIL import Image, ImageDraw, ImageFont
from collections import defaultdict

from app.models.receipts import Receipts
from app.models.activitylog import ActivityLog
from app.models.user import User
from app import db

receipts = Blueprint('receipts', __name__)

def draw_right_aligned(draw_obj, text, x_right, y, font, fill="black"):
    text_width = draw_obj.textlength(text, font=font)
    x_left = x_right - text_width
    draw_obj.text((x_left, y), text, fill=fill, font=font)
    
def draw_center_aligned(draw_obj, text, center_x, y, font, fill="black"):
    text_width = draw_obj.textlength(text, font=font)
    x_left = center_x - (text_width / 2)
    draw_obj.text((x_left, y), text, fill=fill, font=font)
    
def generate_receipt_data(user_id, timeframe='monthly'):
    """Generate the data needed for the receipt"""
    # Query user logs
    user_logs = ActivityLog.query.filter_by(user_id=user_id).all()
    
    # Calculate total hours logged
    total_hours = sum((log.hours or 0) + (log.minutes or 0) / 60 for log in user_logs)
    
    # Calculate category percentages
    category_totals = defaultdict(float)
    for log in user_logs:
        hours = (log.hours or 0) + (log.minutes or 0) / 60
        category_totals[log.category or "Other"] += hours
    
    category_percentages = {}
    for category, hours in category_totals.items():
        percentage = (hours / total_hours) * 100 if total_hours > 0 else 0
        category_percentages[category] = round(percentage)
    
    # Get productive, gaming, and procrastination percentages
    productive_percent = category_percentages.get("Productive", 0)
    gaming_percent = category_percentages.get("Gaming", 0)
    social_percent = category_percentages.get("Social Media", 0)
    other_percent = category_percentages.get("Other", 0)
    
    # Combined procrastination percent (gaming + social + other)
    procrastination_percent = gaming_percent + social_percent + other_percent
    
    # Get current date and time
    now = datetime.now()
    
    # Generate a receipt number (just use timestamp)
    receipt_number = f"{now.strftime('%Y%m%d%H%M%S')}"[-4:]
    
    # Get user info - always use email
    user = User.query.get(user_id)
    user_email = user.email if user and hasattr(user, 'email') else f"User-{user_id}"
    
    # Decide on a status message based on productivity
    if productive_percent >= 70:
        status = "PRODUCTIVITY MASTER"
    elif productive_percent >= 50:
        status = "DOING GOOD"
    elif productive_percent >= 30:
        status = "NEEDS IMPROVEMENT"
    else:
        status = "HELLA BAD BRUH"
    
    # Construct the receipt data
    receipt_data = {
        "date": now.strftime("%a, %b %d, %Y"),
        "time": now.strftime("%I:%M:%S %p"),
        "receipt_number": receipt_number,
        "status": status,
        "customer_name": user_email,  # Use email instead of username
        "procrastination_hours": procrastination_percent,
        "gaming_hours": gaming_percent,
        "productive_hours": productive_percent,
        "total_hours": round(total_hours),
        "operator": "SLOTHIE :)"
    }
    
    return receipt_data

def save_receipt_to_db(user_id):
    """Save receipt data to the database and return the receipt object"""
    # Calculate receipt data
    receipt_data = generate_receipt_data(user_id)
    
    # Check if a receipt already exists for today
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_timestamp = int(today_start.timestamp())
    
    existing_receipt = Receipts.query.filter_by(
        author_id=user_id,
        time=today_timestamp
    ).first()
    
    if existing_receipt:
        # Update existing receipt
        existing_receipt.hours_procrastinated = receipt_data['procrastination_hours']
        existing_receipt.hours_gaming = receipt_data['gaming_hours']
        existing_receipt.hours_productive = receipt_data['productive_hours']
        db.session.commit()
        return existing_receipt
    
    # Create new receipt
    new_receipt = Receipts(
        author_id=user_id,
        time=today_timestamp,
        hours_procrastinated=receipt_data['procrastination_hours'],
        hours_gaming=receipt_data['gaming_hours'],
        hours_productive=receipt_data['productive_hours']
    )
    
    db.session.add(new_receipt)
    db.session.commit()
    
    return new_receipt

def get_receipt_data(user_id, timeframe='monthly'):
    """Get receipt data and the receipt object"""
    # Generate receipt data
    receipt_data = generate_receipt_data(user_id, timeframe)
    
    # Get or create a receipt in the database
    receipt = save_receipt_to_db(user_id)
    
    return receipt_data, receipt

@receipts.route('/download-receipt', methods=['POST'])
@login_required
def download_receipt():
    """Generate and download a receipt PDF"""
    # Get image data from the request
    data = request.json
    image_data = data.get('imageData', '')
    
    # Convert base64 image to binary
    if image_data and ',' in image_data:
        image_data = image_data.split(',')[1]
    
    image_binary = base64.b64decode(image_data)
    
    # Create a PDF from the image
    pdf_buffer = io.BytesIO()
    img = Image.open(io.BytesIO(image_binary))
    img.save(pdf_buffer, format='PDF')
    pdf_buffer.seek(0)
    
    # Return the PDF as a downloadable file
    return send_file(
        pdf_buffer,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=f'productivity_receipt_{datetime.now().strftime("%Y%m%d")}.pdf'
    )

@receipts.route('/receipts/<int:receipt_id>/view', methods=['GET'])
@login_required
def view_receipt(receipt_id):
    """View a specific receipt"""
    receipt = Receipts.query.get_or_404(receipt_id)
    
    # Check if user has permission to view this receipt
    if receipt.author_id != current_user.uid:
        # Check if this receipt was shared with the current user
        from app.models.receipts import ReceiptsShareRequest, Status
        share_request = ReceiptsShareRequest.query.filter_by(
            shared_receipt_id=receipt_id,
            receiver_id=current_user.uid,
            status=Status.ACCEPTED
        ).first()
        
        if not share_request:
            abort(403)
    
    # Get author's email
    author = User.query.get(receipt.author_id)
    author_email = author.email if author and hasattr(author, 'email') else f"User-{receipt.author_id}"
    
    # Create receipt data for display
    receipt_data = {
        "date": datetime.fromtimestamp(receipt.time).strftime("%a, %b %d, %Y"),
        "time": datetime.fromtimestamp(receipt.time).strftime("%I:%M:%S %p"),
        "receipt_number": f"{receipt.receipt_id:04d}",
        "status": get_status_from_productivity(receipt.hours_productive),
        "customer_name": author_email,  # Use email instead of username
        "procrastination_hours": receipt.hours_procrastinated,
        "gaming_hours": receipt.hours_gaming,
        "productive_hours": receipt.hours_productive,
        "oother_categories": receipt.hours_other,
        "total_hours": receipt.hours_procrastinated + receipt.hours_gaming + receipt.hours_productive,
        "operator": "SLOTHIE :)"
    }
    
    return render_template('view_receipt.html', receipt_data=receipt_data, receipt=receipt)

def get_status_from_productivity(productive_percent):
    """Determine status message based on productivity percentage"""
    if productive_percent >= 70:
        return "PRODUCTIVITY MASTER"
    elif productive_percent >= 50:
        return "DOING GOOD"
    elif productive_percent >= 30:
        return "NEEDS IMPROVEMENT"
    else:
        return "HELLA BAD BRUH"

@receipts.route('/receipts/<int:receipt_id>/img', methods=['GET'])
@login_required
def view_receipt_img(receipt_id):
    """Generate and return an image of the receipt"""
    receipt = Receipts.query.get_or_404(receipt_id)
    
    if receipt.author_id != current_user.uid:
        # Check if this receipt was shared with the current user
        from app.models.receipts import ReceiptsShareRequest, Status
        share_request = ReceiptsShareRequest.query.filter_by(
            shared_receipt_id=receipt_id,
            receiver_id=current_user.uid,
            status=Status.ACCEPTED
        ).first()
        
        if not share_request:
            abort(403)
    
    # Get author's email
    author = User.query.get(receipt.author_id)
    author_email = author.email if author and hasattr(author, 'email') else f"User-{receipt.author_id}"
    
    # Create receipt data for image
    receipt_data = {
        "date": datetime.fromtimestamp(receipt.time).strftime("%a, %b %d, %Y"),
        "time": datetime.fromtimestamp(receipt.time).strftime("%I:%M:%S %p"),
        "receipt_number": f"{receipt.receipt_id:04d}",
        "status": get_status_from_productivity(receipt.hours_productive),
        "customer_name": author_email,
        "procrastination_hours": receipt.hours_procrastinated,
        "gaming_hours": receipt.hours_gaming,
        "productive_hours": receipt.hours_productive,
        "total_hours": receipt.hours_procrastinated + receipt.hours_gaming + receipt.hours_productive,
    }
    
    template = os.path.join(current_app.static_folder, 'img', 'receipt-base.png')
    img = Image.open(template)
    draw = ImageDraw.Draw(img)
    
    #need monospace font
    font_path = os.path.join(current_app.static_folder, 'fonts', 'poppins', 'Poppins-Regular.ttf')
    font_small = ImageFont.truetype(font_path, 14)
    font_medium = ImageFont.truetype(font_path, 16)
    font_large = ImageFont.truetype(font_path, 18)
    
    draw_center_aligned(draw, f"{receipt_data['date']} • {receipt_data['time']}", 230, 150, font_small)
    draw_center_aligned(draw, f"#{receipt_data['receipt_number']}", 230, 205, font_medium)

    # Info (needs text alignment adjustment)
    draw.text((260, 300), receipt_data['status'], fill="black", font=font_large)
    draw.text((250, 370), receipt_data['customer_name'], fill="black", font=font_medium)

    # Hours
    draw_right_aligned(draw, f"{receipt_data['procrastination_hours']}%", 410, 490, font_medium)
    draw_right_aligned(draw, f"{receipt_data['gaming_hours']}%", 410, 535, font_medium)
    draw_right_aligned(draw, f"{receipt_data['productive_hours']}%", 410, 575, font_medium)

    # Total
    draw_right_aligned(draw, f"{receipt_data['total_hours']} hrs", 400, 660, font_medium)
    
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    # Return the image
    return send_file(
        img_io, 
        mimetype='image/png',
        as_attachment=False
    )
