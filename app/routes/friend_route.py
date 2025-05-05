import flask
from flask import redirect, session
from flask_login import *
from flask import Blueprint, render_template
from flask_login import login_required, current_user


friends = Blueprint('friends', __name__)
@friends.route('/friend-receipt')
@login_required
def display():

    return flask.render_template('friend-receipt.html')
