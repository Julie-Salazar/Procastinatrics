import flask
from flask import request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import app
from app.models import db
from app.models.user import User


@app.route('/profile-settings')
@login_required
def display():
    return flask.render_template('profile-settings.html')


@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        print("change-password")
        if not current_user.is_password_correct(current_password):
            
            flash('Current password is incorrect.', 'password_change_error')
        elif len(new_password) < 8:
            flash('Current password is too short.', 'password_change_error')

        else:
            
            current_user.set_password(new_password)
            db.session.commit()
            flash('Password updated successfully!', 'password_change_success')
            
            

    return flask.render_template('change-password.html')




@app.route('/change-email', methods=['GET', 'POST'])
@login_required
def change_email():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_email = request.form['new_email']

        if not current_user.is_password_correct(current_password):
            flash('Current password is incorrect.', 'email_change_error')
        else:
            # Optional: check if new_email is already taken
            if db.session.query(User).filter_by(email=new_email).first():
                flash('Email is already in use.', 'email_change_error')
            else:
                current_user.email = new_email
                db.session.commit()
                flash('Email updated successfully!', 'email_change_success')
                

    return flask.render_template('change-email.html')


@app.route('/help', methods=['GET', 'POST'])
@login_required
def help():
    return flask.render_template('help.html')