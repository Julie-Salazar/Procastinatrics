import flask
from flask_login import *
from app import app

@app.route('/log-activity')
@login_required
def upload():

    


    return flask.render_template('log-activity.html')