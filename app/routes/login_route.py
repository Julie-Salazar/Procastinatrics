import flask
from flask_login import *
from app import app
from app.forms import *
from app.database import *
from app.models import *

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return flask.redirect('home')

    form = LoginForm()
    if form.validate_on_submit():
        user = GetUser(email=form.email.data)

        if user is None or not user.is_password_correct(form.password.data):
            return flask.redirect('login')

        login_user(user)
        return flask.redirect('home')

    return flask.render_template("login.html", form=form)
