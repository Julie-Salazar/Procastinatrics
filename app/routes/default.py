import flask
from flask import redirect, url_for
from app import app

@app.route('/')
def default():
    return redirect(url_for('auth.login'))