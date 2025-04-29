import flask
from flask import redirect, session
from flask_login import *
from app import app


@app.route('/analytics-home')
@login_required
def home():


    return flask.render_template('analytics-home.html')