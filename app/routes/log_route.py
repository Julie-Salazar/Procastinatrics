import flask
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db
from app.models.activitylog import ActivityLog

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from forms import LogActivityForm

log = Blueprint('log', __name__)

@log.route('/log-activity', methods=['GET', 'POST'])
@login_required
def log_activity():
    form = LogActivityForm()

    if form.validate_on_submit():
        # Use "other_application" if provided, otherwise use "application"
        app_name = form.other_application.data or form.application.data
        category = form.category.data
        hours = form.hours.data
        minutes = form.minutes.data
        mood = form.mood.data

        # Create a new log entry
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

    return render_template('log-activity.html', form=form)
