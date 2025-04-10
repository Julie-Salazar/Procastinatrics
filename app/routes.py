import flask

from app import app
from .database import *

from .models import *
from .forms import *
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os
from datetime import datetime, date
import sqlalchemy as sa
import pandas as pd



@app.route("/login", methods=["GET", "POST"])
def login():

    # for front end change (uid = 1) to the form input box data : eg user types in password '1234' (uid = form.password)
    if current_user.is_authenticated:
        
        return flask.redirect('home')


    form = LoginForm()

    if form.validate_on_submit():
        user = GetUser(email=form.email.data)

        if user is None:
            # username is not found
            return flask.redirect('login')

        
        if user.is_password_correct(form.password.data) == False:
            return flask.redirect('login')
        
        login_user(user)
        return flask.redirect('home')

    # below for the front end change to (return login.html)
    return flask.render_template("login.html", form=form)


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
