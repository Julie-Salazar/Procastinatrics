from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo, Optional, InputRequired

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

class LogActivityForm(FlaskForm):
    application = SelectField(
        'Application',
        choices=[
            ('', 'Select an application'),
            ('chrome', 'Chrome'),
            ('firefox', 'Firefox'),
            ('discord', 'Discord'),
            # Add other options here...
        ],
        validators=[Optional()]  # Optional because "Other Application" can be used
    )
    other_application = StringField('Other Application', validators=[Optional()])
    category = StringField('Category', validators=[DataRequired()])
    hours = IntegerField('Hours', validators=[DataRequired()])
    minutes = IntegerField('Minutes', validators=[DataRequired()])
    mood = StringField('Mood', validators=[DataRequired()])
    submit = SubmitField('Log Activity')

    def validate(self):
        # Call the default validation first
        if not super().validate():
            return False

        # Ensure either "application" or "other_application" is filled, but not both
        if not self.application.data and not self.other_application.data:
            self.application.errors.append('You must select an application or provide another application.')
            return False
        if self.application.data and self.other_application.data:
            self.other_application.errors.append('You cannot select an application and provide another application at the same time.')
            return False

        return True