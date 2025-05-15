# share_route.py - Fix username reference

from sqlalchemy import select, and_
from flask import Blueprint, render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user

from app.models.receipts import ReceiptsShareRequest, Status, BlockedUsers, Receipts
from app.models.user import User
from app import db

share = Blueprint('share', __name__)

# internal methods
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

@share.route('/share', methods=['GET'])
@login_required
def share_page(users=None):
    from app.routes.receipts_route import get_receipt_data
    
    # Get timeframe from query parameter, default to 'monthly'
    timeframe = request.args.get('timeframe', 'monthly')
    
    if not users:
        users = get_users_sharing(current_user.uid, request.form.get('receipt_id'))
    
    # Get or create receipt data
    receipt_data, receipt = get_receipt_data(current_user.uid, timeframe)
    
    return render_template('share.html', 
                          users=users, 
                          receipt_data=receipt_data,
                          receipt_id=receipt.receipt_id if receipt else None,
                          timeframe=timeframe)

@share.route('/share/send/<int:receipt_id>/<int:target_user_id>', methods=['POST'])
@login_required
def send_request(receipt_id, target_user_id):
    if is_user_blocked(current_user.uid, target_user_id):
        abort(403)
    else:
        exists = ReceiptsShareRequest.query.filter_by(receiver_id=target_user_id, shared_receipt_id=receipt_id, status=Status.PENDING).first()
        if exists: abort(403)
        
        request = ReceiptsShareRequest(
            sender_id=current_user.uid,
            receiver_id=target_user_id,
            shared_receipt_id=receipt_id,
            status=Status.PENDING,
            time=db.func.current_timestamp()
        )
        db.session.add(request)
        db.session.commit()
        return "200"  # Return a string, not an integer

@share.route('/share/requests', methods=['GET'])
@login_required
def share_requests():
    requests = (ReceiptsShareRequest
                .query
                .filter_by(receiver_id=current_user.uid,
                           status=Status.PENDING).all())
    return render_template('share_requests.html', requests=requests)

#Request Interaction APIs
@share.route('/share/requests/accept/<int:request_id>', methods=['POST'])
@login_required
def accept_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.uid: abort(403)
    
    request.status = Status.ACCEPTED
    db.session.commit()
    
    return redirect(url_for('share.share_requests'))

@share.route('/share/requests/decline/<int:request_id>', methods=['POST'])
@login_required
def decline_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.uid: abort(403)
    
    request.status = Status.DECLINED
    db.session.commit()
    
    return redirect(url_for('share.share_requests'))

@share.route('/share/requests/ignore/<int:request_id>', methods=['POST'])
@login_required
def ignore_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.uid: abort(403)
    
    request.status = Status.IGNORED
    db.session.commit()  # Add this line to save the changes
    
    return redirect(url_for('share.share_requests'))