import flask
from flask import redirect, session
from flask_login import *
from app import app

@app.route('/friend-receipt')
@login_required
def display():

    #this prevents cache from being accessed
    if not current_user.is_authenticated:
        return redirect(flask.url_for('/login'))


    return flask.render_template('friend-receipt.html')
