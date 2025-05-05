from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app.models import db
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

auth = Blueprint('auth', __name__)

# ---- Login Form ----
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# ---- Signup Form ----
class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

# ---- Routes ----
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()

        if not user or not user.is_password_correct(password):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('views.analytics_home'))

    return render_template('auth_login.html', form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'warning')
            return redirect(url_for('auth.signup'))

        new_user = User(email=email, usertype='default')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('views.analytics_home'))

    return render_template('auth_signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
