import flask

from app import app
from .database import *

from .models import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from datetime import datetime, date
import sqlalchemy as sa
import pandas as pd



@app.route("/login", methods=["GET", "POST"])
def login():

    # for front end change (uid = 1) to the form input box data : eg user types in password '1234' (uid = form.password)
    user = GetUser(user_name='zac123')
    

    if user is None:
        # username is not found
        return "username not found"
    
    if user.is_password_correct("password1234") == False:
        return "Password is incorrect"
    
    login_user(user)

    # below for the front end change to (return login.html)
    return "logged in as " + user.first_name + " " + user.last_name + " with password " + user.passwordHash


@app.route('/home')
@login_required
def home():
    return flask.render_template('home.html')


@app.route('/share')
@login_required
def share():
    return flask.render_template('share.html')


@app.route('/display')
@login_required
def display():
    return flask.render_template('display.html')

@app.route('/')
def index():
    return flask.redirect(flask.url_for('login'))
