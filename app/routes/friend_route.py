import flask
from flask_login import login_required
from app import app

@app.route('/friend-receipt')
#@login_required
def display():
    return flask.render_template('friend-receipt.html')
