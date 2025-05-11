# from flask import render_template, redirect, session
# from flask_login import *
# from app import app 

# from flask import Blueprint, render_template
# share = Blueprint('share', __name__)


# @share.route('/share')
# @login_required
# def share():

#     # Get friends list, user receipts, etc.
#     friends_list = [
#         {"name": "oogly boogly", "profile_pic": "sloth-hourglass.png"},
#         {"name": "User 2", "profile_pic": "sloth-hourglass.png"},
#     ]
#     return render_template('share.html', friends=friends_list)

from sqlalchemy import select
from flask import Blueprint, render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user

from app.models.receipts import ReceiptsShareRequest, Status
from app.models.user import User
from app import db

share = Blueprint('share', __name__)

@share.route('/share', methods=['GET', 'POST'])
@login_required
def share_page():
    if request.method == 'POST':
        sender_id = current_user.id
        recipient_id = request.form.get('recipient_id')
        receipt_id = request.form.get('receipt_id')
        
        # Check if user exists
        recipient_user = User.query.filter_by(uid=current_user.id).first()
        if not recipient_user: 
            flash("User not found!", 'error')
            abort(403)
        
        # Check if request exists
        query = ReceiptsShareRequest.query.filter_by(sender_id=sender_id,
                                                     recipient_id=recipient_id,
                                                     shared_receipt_id=receipt_id
                                                    ).first()
        if query:
            if query.status != Status.IGNORED: abort(403)
            elif query.status == Status.IGNORED:
                # Update request (resend)
                query.status = Status.PENDING
                query.time = db.func.current_timestamp()
                db.session.add(query)
                db.session.commit()
                flash(f"Resent request to {recipient_user.first_name}!")
                return ('share.html'), 200

        # Create a new share request
        share_request = ReceiptsShareRequest(
            sender_id=current_user.id,
            recipient_id=recipient_id,
            shared_receipt_id=receipt_id,
            status = Status.PENDING,
            time = db.func.current_timestamp()
        )
        
        db.session.add(share_request)
        db.session.commit()
        flash(f"Sent request to {recipient_user.first_name}!", 'success')

    return render_template('share.html'), 200 

@share.route('/share/requests', methods=['GET'])
@login_required
def share_requests():
    requests = (ReceiptsShareRequest
                .query
                .filter_by(receiver_id=current_user.uid,
                           status=Status.PENDING).all())
    return render_template('share_requests.html', requests=requests)

@share.route('/share/requests/<int:request_id>/accept', methods=['POST'])
@login_required
def accept_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.id: abort(403)
    
    request.status = Status.ACCEPTED
    
    return share_requests()

@share.route('/share/requests/<int:request_id>/decline', methods=['POST'])
@login_required
def decline_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.id: abort(403)
    
    request.status = Status.DECLINED
    
    return share_requests()

@share.route('/share/requests/<int:request_id>/ignore', methods=['POST'])
@login_required
def ignore_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.id: abort(403)
    
    request.status = Status.IGNORED
    
    return share_requests()