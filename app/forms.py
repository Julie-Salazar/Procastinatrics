from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length

# this is the form schema for loggin in 
class LoginForm(FlaskForm):
    email = StringField('email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Log In')