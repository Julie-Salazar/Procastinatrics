from app import app,db
from sqlalchemy import text
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models.activitylog import ActivityLog
from app.models.user import User


def init():
    return
    create_hours_view()
    
def create_hours_view():
    sql = """
        CREATE VIEW IF NOT EXISTS hours AS
        SELECT
            activity_log.user_id AS user_id,
            SUM(CASE WHEN activity_log.category = 'procrastination' THEN (activity_log.hours + activity_log.minutes / 60.0) ELSE 0 END) AS procrastination_hours,
            SUM(CASE WHEN activity_log.category = 'gaming' THEN (activity_log.hours + activity_log.minutes / 60.0) ELSE 0 END) AS gaming_hours,
            SUM(CASE WHEN activity_log.category = 'productive' THEN (activity_log.hours + activity_log.minutes / 60.0) ELSE 0 END) AS productive_hours,
            SUM(activity_log.hours + activity_log.minutes / 60.0) AS total_hours_logged
        FROM activity_log
        GROUP BY activity_log.user_id;
    """
    with db.engine.connect() as connection:
        connection.execute(text(sql))



        
        