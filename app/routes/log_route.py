import flask
from flask_login import *
from app import app

@app.route('/log-activity')
@login_required
def log_activity():
    if request.method == 'POST':
        app_name = request.form.get('application')
        category = request.form.get('category')
        hours = int(request.form.get('hours', 0))
        minutes = int(request.form.get('minutes', 0))
        mood = request.form.get('mood')

        new_log = ActivityLog(
            user_id=current_user.id,
            application=app_name,
            category=category,
            hours=hours,
            minutes=minutes,
            mood=mood
        )
        db.session.add(new_log)
        db.session.commit()
        flash('Activity logged successfully.', 'success')
        return redirect(url_for('views.analytics_home'))
    
    

    return render_template('log-activity.html')





