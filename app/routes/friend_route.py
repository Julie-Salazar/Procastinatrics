import flask
from flask import redirect, session
from flask_login import *
from app import app

@app.route('/friend-receipt')
@login_required
def display():

    


    return flask.render_template('friend-receipt.html')
