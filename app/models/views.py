from app import app,db
from sqlalchemy import text

def init():
    create_hours_view()
    
def create_hours_view():
    sql = """
        CREATE VIEW IF NOT EXISTS hours AS
        SELECT
            mood.author_id AS user_id,
            SUM(CASE WHEN mood.app_type = 'procrastination' THEN mood.time_spent ELSE 0 END) AS procrastination_hours,
            SUM(CASE WHEN mood.app_type = 'gaming' THEN mood.time_spent ELSE 0 END) AS gaming_hours,
            SUM(CASE WHEN mood.app_type = 'productive' THEN mood.time_spent ELSE 0 END) AS productive_hours
        FROM mood
        GROUP BY mood.author_id;
    """
    with db.engine.connect() as connection:
        connection.execute(text(sql))
        
        