from flask import render_template, redirect, session
from flask_login import *
from app import app 

@app.route('/share')
@login_required
def share():


    #this prevents cache from being accessed
    if not current_user.is_authenticated:
        return redirect(flask.url_for('/login'))

    # Get friends list, user receipts, etc.
    friends_list = [
        {"name": "oogly boogly", "profile_pic": "sloth-hourglass.png"},
        {"name": "User 2", "profile_pic": "sloth-hourglass.png"},
    ]
    return render_template('share.html', friends=friends_list)