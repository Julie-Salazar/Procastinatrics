
from flask import Blueprint, render_template, request, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.receipts import ReceiptsShareRequest, Status, Receipts
from app.models.user import User
from app.models.activitylog import ActivityLog
from app import db
from datetime import datetime
from collections import defaultdict

friends = Blueprint('friends', __name__)

from datetime import datetime

@friends.app_template_filter('timestamp_to_date')
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

@friends.app_template_filter('timestamp_to_time')
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


def calculate_percentages(user_id):
    user_logs = ActivityLog.query.filter_by(user_id=user_id).all()
    total_hours = sum((log.hours or 0) + (log.minutes or 0) / 60 for log in user_logs)

    category_totals = defaultdict(float)
    for log in user_logs:
        hours = (log.hours or 0) + (log.minutes or 0) / 60
        category_totals[log.category or "Other"] += hours

    category_percentages = {
        category: round((hours / total_hours) * 100) if total_hours > 0 else 0
        for category, hours in category_totals.items()
    }

    productive_percent = category_percentages.get("Productive", 0)
    gaming_percent = category_percentages.get("Gaming", 0)
    social_percent = category_percentages.get("Social Media", 0)
    other_percent = category_percentages.get("Other", 0)
    procrastination_percent = social_percent + other_percent

    return {
        "procrastination_percent": procrastination_percent,
        "gaming_percent": gaming_percent,
        "productive_percent": productive_percent,
        "other_percent": other_percent,
        "total_hours": round(total_hours)
    }

@friends.route('/friend-receipt')
@login_required
def display_receipts():
    accepted_requests = ReceiptsShareRequest.query.filter_by(
        receiver_id=current_user.uid,
        status=Status.ACCEPTED
    ).all()

    friend_receipts = []

    for request in accepted_requests:
        sender = User.query.get(request.sender_id)
        receipt = Receipts.query.get(request.shared_receipt_id)

        if sender and receipt:
            # Always calculate total hours from logs
            user_logs = ActivityLog.query.filter_by(user_id=receipt.author_id).all()
            total_hours = sum((log.hours or 0) + (log.minutes or 0) / 60 for log in user_logs)
            total_hours = round(total_hours)

            if all(v == 0 for v in [
                receipt.hours_procrastinated,
                receipt.hours_gaming,
                receipt.hours_productive
            ]):
                # Get fresh percentages from logs
                percentages = calculate_percentages(receipt.author_id)
                receipt.hours_procrastinated = percentages["procrastination_percent"]
                receipt.hours_gaming = percentages["gaming_percent"]
                receipt.hours_productive = percentages["productive_percent"]
                db.session.commit()

                # Use updated percentages
                procrastination = percentages["procrastination_percent"]
                gaming = percentages["gaming_percent"]
                productive = percentages["productive_percent"]
            else:
                # Use stored values
                procrastination = receipt.hours_procrastinated
                gaming = receipt.hours_gaming
                productive = receipt.hours_productive

            friend_receipts.append({
                'request_id': request.request_id,
                'sender': sender,
                'receipt': receipt,
                'time_shared': request.time,
                'total_hours': total_hours,
                'procrastination_percent': procrastination,
                'gaming_percent': gaming,
                'productive_percent': productive
            })

    return render_template('friend-receipt.html', friend_receipts=friend_receipts)
