import flask
from flask_login import *
from app import app

@app.route('/log-activity')
@login_required
def upload():

    #this prevents cache from being accessed
    if not current_user.is_authenticated:
        return redirect(flask.url_for('/login'))


    return flask.render_template('log-activity.html')