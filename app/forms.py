from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileRequired
from wtforms import EmailField, PasswordField, BooleanField, SubmitField, SelectField, SelectMultipleField, HiddenField, FileField, DateField, widgets, TextAreaField, StringField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Length, Email, EqualTo, Optional, InputRequired

from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, Optional
# this is the form schema for loggin in 
class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Log In')
    remember_me = BooleanField('Remember Me')

from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, IntegerField, HiddenField, SubmitField
from wtforms.validators import DataRequired, NumberRange

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
    ('productive', 'Productive'),
    ('social_media', 'Social Media'),
    ('gaming', 'Gaming'),
    ('other', 'Other')
]

class LogActivityForm(FlaskForm):
    application = SelectField('Application', choices=application_choices, validators=[Optional()])
    other_application = StringField('Other Application')
    category = SelectField('Category', choices=category_choices, validators=[Optional()])
    hours = IntegerField('Hours', validators=[DataRequired(), NumberRange(min=0, max=24)])
    minutes = IntegerField('Minutes', validators=[DataRequired(), NumberRange(min=0, max=59)])
    mood = HiddenField('Mood', default='😊')
    submit = SubmitField('Submit')
