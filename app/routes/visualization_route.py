import flask
from flask_login import login_required
from app import app

@app.route('/display')
@login_required
def display():
    return flask.render_template('display.html')
