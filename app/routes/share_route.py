# share_route.py - Fix username reference

from sqlalchemy import select, and_
from flask import Blueprint, render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from collections import defaultdict

from app.models.receipts import ReceiptsShareRequest, Status, BlockedUsers, Receipts
from app.models.user import User
from app.models.activitylog import ActivityLog
from app import db

share = Blueprint('share', __name__)

# internal methods
def get_pending_requests():
    return (ReceiptsShareRequest
            .query
            .filter_by(receiver_id=current_user.uid,
                       status=Status.PENDING).all())

def get_blocked_users_id(user_id):
    blocked_list = BlockedUsers.query.filter(BlockedUsers.blocker_id == user_id).all()
    return [blocked.target_user_id for blocked in blocked_list]

def is_user_blocked(user_id, target_id):
    blocked_list = BlockedUsers.query.filter(BlockedUsers.blocker_id == target_id, BlockedUsers.target_user_id == user_id).first()
    if blocked_list: return True
    return False
    
def get_users_sharing(user_id, receipt_id):
    users = User.query.filter(User.uid != user_id).all()
    
    # block query
    blocked_id = get_blocked_users_id(user_id)
    
    # user filtering
    # TODO efficient current-request handler that doesnt involve requerying every loop
    users = [user for user in users if user.uid not in blocked_id]
    
    return users


@share.app_template_filter('timestamp_to_date')
def timestamp_to_date(value, format='%a, %b %d, %Y'):
    try:
        if hasattr(value, 'strftime'):
            return value.strftime(format)
        # Try parsing string to datetime
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif isinstance(value, (int, float)):
            value = datetime.fromtimestamp(value)
        return value.strftime(format)
    except (ValueError, TypeError):
        return "Date unavailable"

@share.app_template_filter('timestamp_to_time')
def timestamp_to_time(value, format='%I:%M:%S %p'):
    try:
        if hasattr(value, 'strftime'):
            return value.strftime(format)
        if isinstance(value, str):
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        elif isinstance(value, (int, float)):
            value = datetime.fromtimestamp(value)
        return value.strftime(format)
    except (ValueError, TypeError):
        return "Time unavailable"


# Updated share_page function for share_route.py

# Updated share_page function to use improved percentages

@share.route('/share', methods=['GET'])
@login_required
def share_page():
    """Routing function for /share, generates receipt upon sharing.

    Returns:
        HTML file for share with a receipt.
    """
    from app.routes.receipts_route import get_receipt_data
    from app.utils.receipt_helper import calculate_percentages
    
    # Get timeframe from query parameter, default to 'monthly'
    timeframe = request.args.get('timeframe', 'monthly')
    
    # Always calculate fresh percentages
    percentages = calculate_percentages(current_user.uid)
    
    # Get receipt data (which might use old percentages)
    receipt_data, receipt = get_receipt_data(current_user.uid, timeframe)
    current_time = datetime.now()
    receipt_data["date"] = current_time.strftime("%a, %b %d, %Y")
    receipt_data["time"] = current_time.strftime("%I:%M:%S %p")
    # Update receipt_data with the fresh percentages
    receipt_data["procrastination_hours"] = percentages["procrastination_percent"]
    receipt_data["gaming_hours"] = percentages["gaming_percent"]
    receipt_data["productive_hours"] = percentages["productive_percent"]
    receipt_data["total_hours"] = percentages["total_hours"]
    
    # Update the receipt in database if needed
    if receipt and (
        receipt.hours_procrastinated == 0 and
        receipt.hours_gaming == 0 and
        receipt.hours_productive == 0
    ):
        receipt.hours_procrastinated = percentages["procrastination_percent"]
        receipt.hours_gaming = percentages["gaming_percent"]
        receipt.hours_productive = percentages["productive_percent"]
        db.session.commit()
        print(f"DEBUG - Updated receipt in database with new percentages")
    
    # Debug the final receipt_data being sent to template
    print("\nDEBUG - Final receipt_data being sent to template:")
    for key, value in receipt_data.items():
        print(f"  {key}: {value}")
    
    return render_template(
        'share.html',
        users=get_users_sharing(current_user.uid, request.form.get('receipt_id')),
        receipt_data=receipt_data,
        receipt_id=receipt.receipt_id if receipt else None,
        timeframe=timeframe
    )

@share.route('/share/send/<int:receipt_id>/<int:target_user_id>', methods=['POST'])
@login_required
def send_request(receipt_id, target_user_id):
    """Routing for sending a receipt share request.

    Args:
        receipt_id (int): receipt_id to be shared.
        target_user_id (int): user_id to send a request to.

    Returns:
        redirects to /share
    """
    if is_user_blocked(current_user.uid, target_user_id):
        abort(403)

    existing_request = ReceiptsShareRequest.query.filter_by(
        receiver_id=target_user_id,
        shared_receipt_id=receipt_id,
        status=Status.PENDING
    ).first()

    if existing_request:
        flash("A pending request for this receipt already exists.", "warning")
        return redirect(url_for('share.share_page'))

    # 🧾 Fetch the receipt
    receipt = db.session.get(Receipts,receipt_id)
    if not receipt:
        flash("Receipt not found.", "danger")
        return redirect(url_for('share.share_page'))

    print(f"DEBUG - Preparing to share receipt {receipt_id} with user {target_user_id}")
    print(f"  Current Values → P: {receipt.hours_procrastinated}%, G: {receipt.hours_gaming}%, Prod: {receipt.hours_productive}%")

    # ♻️ Recalculate if all values are zero
    if (
        receipt.hours_procrastinated == 0 and 
        receipt.hours_gaming == 0 and 
        receipt.hours_productive == 0
    ):
        from app.routes.friend_route import calculate_percentages
        percentages = calculate_percentages(receipt.author_id)

        receipt.hours_procrastinated = percentages["procrastination_percent"]
        receipt.hours_gaming = percentages["gaming_percent"]
        receipt.hours_productive = percentages["productive_percent"]
        db.session.commit()

        print(f"DEBUG - Recalculated and updated receipt {receipt_id} before sharing")

    # ➕ Create new share request
    new_request = ReceiptsShareRequest(
        sender_id=current_user.uid,
        receiver_id=target_user_id,
        shared_receipt_id=receipt_id,
        status=Status.PENDING,
        time=db.func.current_timestamp()
    )

    db.session.add(new_request)
    db.session.commit()

    print(f"✅ Share request #{new_request.request_id} created: receipt {receipt_id} → user {target_user_id}")
    flash("Receipt shared successfully!", "success")
    return redirect(url_for('share.share_page'))



@share.route('/share/requests', methods=['GET'])
@login_required
def share_requests():
    """Route for share requests.

    Returns:
        HTML file for /share/requests
    """
    requests = (ReceiptsShareRequest
                .query
                .filter_by(receiver_id=current_user.uid,
                           status=Status.PENDING).all())
    return render_template('share_requests.html', requests=requests)

#Request Interaction APIs
@share.route('/share/requests/accept/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    """Route function to accept request_id

    Args:
        request_id (int): request_id to be accepted.

    Returns:
        redirects to /share/requests
    """
    request = db.session.get(ReceiptsShareRequest,request_id)
    if request.receiver_id != current_user.uid: abort(403)
    
    request.status = Status.ACCEPTED
    db.session.commit()
    
    return redirect(url_for('share.share_requests'))

@share.route('/share/requests/decline/<int:request_id>', methods=['POST'])
@login_required
def decline_request(request_id):
    """Route function to decline request_id, blocks user from sending another request to the decliner.

    Args:
        request_id (int): request_id to be declined.

    Returns:
        redirects to /share/requests
    """
    request = db.session.get(ReceiptsShareRequest,request_id)
    if request.receiver_id != current_user.uid: abort(403)
    
    request.status = Status.DECLINED
    db.session.commit()
    
    return redirect(url_for('share.share_requests'))

@share.route('/share/requests/ignore/<int:request_id>', methods=['POST'])
@login_required
def ignore_request(request_id):
    """Route function to ignore request_id. Ignoring allows the user to resend another duplicate request.

    Args:
        request_id (int): request_id to be ignored.

    Returns:
        redirects to /share/requests
    """
    request = db.session.get(ReceiptsShareRequest,request_id)
    if request.receiver_id != current_user.uid: abort(403)
    
    request.status = Status.IGNORED
    db.session.commit()  # Add this line to save the changes
    
    return redirect(url_for('share.share_requests'))