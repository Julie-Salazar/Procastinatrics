import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db
from app.models.activitylog import ActivityLog

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

log = Blueprint('log', __name__)

@log.route('/log-activity', methods=['GET', 'POST'])
@login_required
def log_activity():
    if request.method == 'POST':
        app_name = request.form.get('application')
        category = request.form.get('category')
        hours = int(request.form.get('hours', 0))
        minutes = int(request.form.get('minutes', 0))
        mood = request.form.get('mood')

        new_log = ActivityLog(
            user_id=current_user.id,
            application=app_name,
            category=category,
            hours=hours,
            minutes=minutes,
            mood=mood
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Activity logged successfully.', 'success')
        return redirect(url_for('views.analytics_home'))
    
    

    return render_template('log-activity.html')




# FOR TMORROW MAKE SURE THAT YOU TAKE OFF THE BACK BUTTON >> HAVE NAME INPUT ONLY FOR SIGNUP SO THAT IT SHOWS WHEN LOGGING IN 

