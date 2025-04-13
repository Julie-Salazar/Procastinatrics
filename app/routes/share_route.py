import flask
from flask_login import login_required
from app import app

@app.route('/share')
@login_required
def share():
    return flask.render_template('share.html')
