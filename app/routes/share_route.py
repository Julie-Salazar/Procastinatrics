from flask import render_template
from app import app 

@app.route('/share')

def share():
    # Get friends list, user receipts, etc.
    friends_list = [
        {"name": "oogly boogly", "profile_pic": "sloth-hourglass.png"},
        {"name": "User 2", "profile_pic": "sloth-hourglass.png"},
    ]
    return render_template('share.html', friends=friends_list)