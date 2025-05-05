from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/analytics-home')
@login_required
def analytics_home():
    return render_template('analytics-home.html', user=current_user)
