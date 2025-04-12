import flask
from flask_login import login_required
from app import app

@app.route('/home')
@login_required
def home():
    return flask.render_template('home.html')