from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo

# this is the form schema for loggin in 
class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Log In')
    remember_me = BooleanField('Remember Me')

# this is the form schema for signing up 
class SignupForm(FlaskForm):
    email = EmailField('Email',validators=[DataRequired(),Email(message='Please enter a valid email address')])
    password = PasswordField('Create a password',validators=[DataRequired(message="Password can't be empty"), Length(min=8, message='Password must be at least 8 characters long')])
    confirm_password = PasswordField('Confirm password',validators=[DataRequired(message='Enter password again'),EqualTo('password', message='Must be equal to password')])
    submit = SubmitField('Sign Up')