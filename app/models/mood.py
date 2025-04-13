from app import db
from . import User

class Mood(db.Model):   
    mood_id = db.Column("mood_id",db.Integer,primary_key=True)
    author_id = db.Column("author_id",db.Integer,db.ForeignKey(User.id))
    app_name = db.Column("app_name",db.String(50))
    app_type = db.Column("app_type",db.String(20),nullable=False)
    minutes_spent = db.Column("minutes_spent",db.Integer)
    mood_emoji = db.Column("mood_emoji",db.String(10))

