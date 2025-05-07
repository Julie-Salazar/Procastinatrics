from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models.activitylog import ActivityLog



views = Blueprint('views', __name__)

@views.route('/analytics-home')
@login_required
def analytics_home():
    recent_logs = ActivityLog.query.filter_by(user_id=current_user.uid) \
                                   .order_by(ActivityLog.timestamp.desc()) \
                                   .limit(8).all()
    return render_template('analytics-home.html', user=current_user, recent_logs=recent_logs)
