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


from flask import Blueprint, render_template, request
from flask_login import login_required

share = Blueprint('share', __name__)

@share.route('/share', methods=['GET', 'POST'])
@login_required
def share_page():
    if request.method is 'POST':
        #TODO
        pass

    return render_template('share.html')  # update this if your template name is different
