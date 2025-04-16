import flask
from flask_login import *
from app import app
from app.forms import *
from app.database import *
from app.models import *

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = GetUser(email=form.email.data)

        if user is None or not user.is_password_correct(form.password.data):
            return flask.redirect('login')

        login_user(user)


    return flask.render_template("login.html", form=form)

@app.route('/forgot-password')
def forgot_password():
    return "Forgot Password page placeholder"

@app.route('/login_facebook')
def login_facebook():
    return "Login Facebook page placeholder"

@app.route('/login_google')
def login_google():
    return "Login Google page placeholder"

@app.route('/signup')
def signup():
    return "Sign Up page placeholder"