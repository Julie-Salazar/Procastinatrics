import flask
from flask_login import login_required
from app import app

@app.route('/upload')
@login_required
def upload():
    return flask.render_template('upload.html')