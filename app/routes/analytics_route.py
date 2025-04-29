import flask
from flask import redirect, session
from flask_login import *
from app import app


@app.route('/analytics-home')
@login_required
def home():


    #this prevents cache from being accessed
    if not current_user.is_authenticated:
        return redirect(flask.url_for('/login'))

    return flask.render_template('analytics-home.html')