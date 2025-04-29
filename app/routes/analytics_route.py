import flask
from flask_login import login_required
from app import app

@app.route('/analytics-home')
@login_required
def home():
    return flask.render_template('analytics_home.html')