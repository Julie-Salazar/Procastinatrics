import flask
from flask import url_for, flash, redirect, render_template 
from flask_login import current_user, login_user, logout_user 
from app import app, db 
from app.forms import LoginForm, SignupForm 
from app.database import GetUser 
from app.models import User 

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return flask.redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = GetUser(email=form.email.data)

        if user is None or not user.is_password_correct(form.password.data):
            return flask.redirect('login')

        login_user(user)
        return flask.redirect(url_for('home'))

    return flask.render_template("auth_login.html", form=form)


# --- Haven't implemented ---
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm() 
    return render_template("auth_signup.html", form=form)

# --- Haven't implemented ---
@app.route('/forgot-password')
def forgot_password():
    return "Forgot Password page placeholder"

# --- Haven't implemented ---
@app.route('/login_facebook')
def login_facebook():
    return "Login Facebook page placeholder"

# --- Haven't implemented ---
@app.route('/login_google')
def login_google():
    return "Login Google page placeholder"
