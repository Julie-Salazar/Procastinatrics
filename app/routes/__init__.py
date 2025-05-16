from .login_route import *
from .analytics_route import *
from .share_route import *
from .friend_route import *
from .log_route import *

from app import app

from flask import Flask

from app.routes import analytics_route, profile_settings_route, share_route, friend_route, log_route

app.config['SECRET_KEY'] = 'your-secret-key'

@app.context_processor
def inject_requests():
    if current_user.is_authenticated:
        return {'requests': get_pending_requests()}
    return {'requests': []}



@app.context_processor
def inject_pending_requests():
    if current_user.is_authenticated:
        requests = (db.session.query(ReceiptsShareRequest, User)
                    .join(User, ReceiptsShareRequest.sender_id == User.uid)
                    .filter(ReceiptsShareRequest.receiver_id == current_user.uid,
                            ReceiptsShareRequest.status == Status.PENDING)
                    .all())

        pending_requests = [{
            'request_id': req.request_id,
            'sender_username': user.first_name
        } for req, user in requests]

        return {'pending_share_requests': pending_requests}
    return {'pending_share_requests': []}

