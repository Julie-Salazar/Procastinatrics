from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db
from app.models.activitylog import ActivityLog
from app.forms import LogActivityForm
from datetime import datetime

log = Blueprint('log', __name__)

@log.route('/log-activity', methods=['GET', 'POST'])
@login_required
def log_activity():
    form = LogActivityForm()

    if form.validate_on_submit():
        # Application logic
        app_name = form.application.data
        if app_name == 'other':
            if not form.other_application.data.strip():
                flash('Please provide a name for the other application.', 'warning')
                return render_template('log-activity.html', form=form)

            app_name = form.other_application.data.strip()

        # Category logic
        category = form.category.data
        if category == 'other':
            if not form.other_category.data.strip():
                flash('Please provide a name for the other category.', 'warning')
                return render_template('log-activity.html', form=form)
            category = form.other_category.data.strip()


        new_log = ActivityLog(
            user_id=current_user.id,
            application=app_name,
            category=category,
            hours=form.hours.data,
            minutes=form.minutes.data,
            mood=form.mood.data,
            timestamp=datetime.utcnow()
        )

        db.session.add(new_log)
        db.session.commit()
        flash('Activity logged successfully!', 'success')
        return redirect(url_for('views.analytics_home'))


    return render_template('log-activity.html', form=form)

