from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets, TextAreaField, StringField, IntegerField
from wtforms import StringField, EmailField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets, TextAreaField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo, Optional, InputRequired, NumberRange

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


# Choices for the application dropdown
application_choices = [
    ('', 'Select an application'),
    ('chrome', 'Chrome'), ('firefox', 'Firefox'), ('safari', 'Safari'), ('edge', 'Microsoft Edge'),
    ('discord', 'Discord'), ('slack', 'Slack'), ('instagram', 'Instagram'), ('facebook', 'Facebook'),
    ('twitter', 'Twitter'), ('tiktok', 'TikTok'), ('snapchat', 'Snapchat'), ('whatsapp', 'WhatsApp'),
    ('telegram', 'Telegram'), ('zoom', 'Zoom'), ('teams', 'Microsoft Teams'), ('vscode', 'VS Code'),
    ('word', 'Microsoft Word'), ('excel', 'Microsoft Excel'), ('powerpoint', 'PowerPoint'),
    ('outlook', 'Outlook'), ('gmail', 'Gmail'), ('googledocs', 'Google Docs'), ('googlesheets', 'Google Sheets'),
    ('photoshop', 'Photoshop'), ('illustrator', 'Illustrator'), ('figma', 'Figma'),
    ('netflix', 'Netflix'), ('hulu', 'Hulu'), ('disney', 'Disney+'), ('youtube', 'YouTube'),
    ('twitch', 'Twitch'), ('spotify', 'Spotify'), ('appletv', 'Apple TV'), ('amazonprime', 'Amazon Prime Video'),
    ('steam', 'Steam'), ('epicgames', 'Epic Games'), ('leagueoflegends', 'League of Legends'),
    ('minecraft', 'Minecraft'), ('fortnite', 'Fortnite'), ('valorant', 'Valorant'), ('roblox', 'Roblox'),
    ('apexlegends', 'Apex Legends'), ('battlenet', 'Battle.net'), ('origin', 'EA Origin'),
    ('other', 'Other')
]

# Choices for the category dropdown
category_choices = [
    ('', 'Select a category'),
    ('productive', 'Productive'),
    ('social_media', 'Social Media'),
    ('gaming', 'Gaming'),
    ('other', 'Other')
]

class LogActivityForm(FlaskForm):
    application = SelectField('Application', choices=application_choices, validators=[DataRequired()])
    other_application = StringField('Other Application')
    category = SelectField('Category', choices=category_choices, validators=[DataRequired()])
    other_category = StringField('Other Category')
    hours = IntegerField('Hours', validators=[DataRequired(), NumberRange(min=0, max=24)])
    minutes = IntegerField('Minutes', validators=[DataRequired(), NumberRange(min=0, max=59)])
    mood = HiddenField('Mood', default='😊')

    # Submit button
    submit = SubmitField('Submit')
