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

from sqlalchemy import select,and_
from flask import Blueprint, render_template, request, flash, abort, redirect, url_for
from flask_login import login_required, current_user

from app.models.receipts import ReceiptsShareRequest, Status, BlockedUsers
from app.models.user import User
from app import db

share = Blueprint('share', __name__)

# internal methods
def get_blocked_users_id(user_id):
    blocked_list = BlockedUsers.query.filter(BlockedUsers.blocker_id == user_id).all()
    return [blocked.target_user_id for blocked in blocked_list]

def is_user_blocked(user_id,target_id):
    blocked_list = BlockedUsers.query.filter(BlockedUsers.blocker_id == target_id, BlockedUsers.target_user_id == user_id).first()
    if blocked_list: return True
    return False
    
    
def get_users_sharing(user_id,receipt_id):
    users = User.query.filter(User.uid != user_id).all()
    
    #block query
    blocked_id = get_blocked_users_id(user_id)
    
    #user filtering
    ##TODO efficient current-request handler that doesnt involve requerying every loop
    users = [user for user in users if user.uid not in blocked_id]
    
    return users

@share.route('/share', methods=['GET'])
@login_required
def share_page(users=None):
    if not users:
        users = get_users_sharing(current_user.id,request.form.get('receipt_id'))

    return render_template('share.html', users=users)

@share.route('/share/send/<int:receipt_id>/<int:target_user_id>', methods=['POST'])
@login_required
def send_request(receipt_id, target_user_id):
    if is_user_blocked(current_user.uid,target_user_id):
        abort(403)
    else:
        exists = ReceiptsShareRequest.query.filter_by(receiver_id=target_user_id,shared_receipt_id=receipt_id,status=Status.PENDING).first()
        if exists: abort(403)
        
        request = ReceiptsShareRequest(sender_id=current_user.uid,
                                       receiver_id=target_user_id,
                                       shared_receipt_id=receipt_id,
                                       status=Status.PENDING,
                                       time=db.func.current_timestamp()
                                       )
        db.session.add(request)
        db.session.commit()
        return 200


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
    if request.receiver_id != current_user.id: abort(403)
    
    request.status = Status.ACCEPTED
    
    return share_requests()

@share.route('/share/requests/decline/<int:request_id>', methods=['POST'])
@login_required
def decline_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.id: abort(403)
    
    request.status = Status.DECLINED
    
    return share_requests()

@share.route('/share/requests/ignore/<int:request_id>', methods=['POST'])
@login_required
def ignore_request(request_id):
    request = ReceiptsShareRequest.query.get_or_404(request_id)
    if request.receiver_id != current_user.id: abort(403)
    
    request.status = Status.IGNORED
    
    return share_requests()