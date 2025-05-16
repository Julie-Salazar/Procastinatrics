
# --------------------- 1. friend_route.py ---------------------

from flask import Blueprint, render_template, request, abort, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app.models.receipts import ReceiptsShareRequest, Status, Receipts
from app.models.user import User
from app.models.activitylog import ActivityLog
from app import db
from datetime import datetime
from collections import defaultdict
from flask import jsonify, flash


friends = Blueprint('friends', __name__)



@friends.app_template_filter('timestamp_to_date')
def timestamp_to_date(timestamp, format='%a, %b %d, %Y'):
    """Convert a Unix timestamp to a formatted date string"""
    try:
        if timestamp:
            return datetime.fromtimestamp(int(timestamp)).strftime(format)
        return "Date unavailable"
    except (ValueError, TypeError):
        return "Date unavailable"

@friends.app_template_filter('timestamp_to_time')
def timestamp_to_time(timestamp, format='%I:%M:%S %p'):
    """Convert a Unix timestamp to a formatted time string"""
    try:
        if timestamp:
            return datetime.fromtimestamp(int(timestamp)).strftime(format)
        return "Time unavailable"
    except (ValueError, TypeError):
        return "Time unavailable"

def calculate_percentages(user_id):
    """Calculate the actual percentages for a user from their activity logs"""
    # Query user logs
    user_logs = ActivityLog.query.filter_by(user_id=user_id).all()
    
    # Debug print
    print(f"DEBUG - ActivityLog count for user {user_id}: {len(user_logs)}")
    
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
    procrastination_percent = social_percent + other_percent
    
    print(f"DEBUG - Calculated percentages for user {user_id}:")
    print(f"  Total hours: {total_hours}")
    print(f"  Procrastination: {procrastination_percent}%")
    print(f"  Gaming: {gaming_percent}%")
    print(f"  Productive: {productive_percent}%")
    
    return {
        "procrastination_percent": procrastination_percent,
        "gaming_percent": gaming_percent,
        "productive_percent": productive_percent,
        "total_hours": round(total_hours)
    }


@friends.route('/friend-receipt')
@login_required
def display_receipts():
    """
    Display a list of all accepted receipt shares from friends
    """
    # Get all accepted receipt share requests where the current user is the receiver
    accepted_requests = ReceiptsShareRequest.query.filter_by(
    receiver_id=current_user.uid,
    status=Status.ACCEPTED
    ).all()

    print(f"[DEBUG] {len(accepted_requests)} accepted requests")
    for r in accepted_requests:
        print(f"Request ID: {r.request_id} | Receipt ID: {r.shared_receipt_id} | Sender ID: {r.sender_id} | Time: {r.time}")

    
    # Create a list with sender information and receipt data
    friend_receipts = []
    
    print(f"[SHARE DEBUG] {len(accepted_requests)} accepted shares found")
    for request in accepted_requests:
        print(f" - Request #{request.request_id} | receipt_id={request.shared_receipt_id} | from={request.sender_id} to={request.receiver_id}")

        # Get the sender's information
        sender = User.query.get(request.sender_id)
        
        # Get the receipt information
        receipt = Receipts.query.get(request.shared_receipt_id)
        
        if sender and receipt:
            # Debug print receipt data to server logs
            print(f"DEBUG - Reading Receipt {receipt.receipt_id}, sender: {sender.email}")
            print(f"  Time: {receipt.time}")
            print(f"  Procrastination: {receipt.hours_procrastinated}")
            print(f"  Gaming: {receipt.hours_gaming}")
            print(f"  Productive: {receipt.hours_productive}")
            
            # If percentages are all zero or very low, try to calculate them
            if (receipt.hours_procrastinated == 0 and 
                receipt.hours_gaming == 0 and 
                receipt.hours_productive == 0):
                print(f"DEBUG - All percentages are zero for receipt {receipt.receipt_id}, calculating from logs")
                
                # Try to calculate from author's logs
                percentages = calculate_percentages(receipt.author_id)
                
                # If calculated percentages are non-zero, update receipt
                if (percentages["procrastination_percent"] > 0 or 
                    percentages["gaming_percent"] > 0 or 
                    percentages["productive_percent"] > 0):
                    
                    # Update the receipt object with calculated percentages
                    receipt.hours_procrastinated = percentages["procrastination_percent"]
                    receipt.hours_gaming = percentages["gaming_percent"] 
                    receipt.hours_productive = percentages["productive_percent"]
                    
                    # Save to database
                    db.session.commit()
                    print(f"DEBUG - Updated receipt {receipt.receipt_id} with calculated percentages")
                else:
                    # If still zero, set some default values for better visualization
                    print(f"DEBUG - Setting default values for receipt {receipt.receipt_id}")
                    receipt.hours_procrastinated 
                    receipt.hours_gaming 
                    receipt.hours_productive 

                    # Not committing these default values to database
            print(f"[ROUTE DEBUG] Found {len(accepted_requests)} accepted requests")

            for r in accepted_requests:
                print(f"Request ID: {r.request_id}, Receipt ID: {r.shared_receipt_id}, Sender ID: {r.sender_id}, Receiver ID: {r.receiver_id}, Status: {r.status}")

            friend_receipts.append({
                'request_id': request.request_id,
                'sender': sender,
                'receipt': receipt,
                'time_shared': request.time
            })

            # return jsonify([
            #     {
            #         "request_id": f['request_id'],
            #         "receipt_id": f['receipt'].receipt_id,
            #         "sender": f['sender'].email,
            #         "time_shared": f['time_shared']
            #     } for f in friend_receipts
            # ])
        flash(f"{len(friend_receipts)} shared receipts loaded.", "info")

    
    return render_template('friend-receipt.html', 
                          friend_receipts=friend_receipts)

# @friends.route('/friend-receipt/remove/<int:request_id>', methods=['POST'])
# @login_required
# def remove_shared_receipt(request_id):
#     """
#     Remove a shared receipt from your list (change status to REMOVED)
#     """
#     request = ReceiptsShareRequest.query.get_or_404(request_id)
    
#     # Check if the current user is the receiver
#     if request.receiver_id != current_user.uid:
#         abort(403)  # Forbidden
    
#     # Change status to removed
#     request.status = Status.REMOVED
#     db.session.commit()
    
#     flash('The shared receipt has been removed from your list.', 'success')
#     return redirect(url_for('friends.display_receipts'))
