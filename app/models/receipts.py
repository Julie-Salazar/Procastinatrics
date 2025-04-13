from app import db
from . import User

class Receipts(db.Model):
    """
    Stores data instead of accessing other tables.
    """
    receipt_id = db.Column("receipt_id",db.Integer,primary_key=True)
    author_id = db.Column("author_id",db.Integer,db.ForeignKey(User.id))
    time = db.Column("time",db.Integer)
    hours_procrastinated = db.Column("hours_procrastinated",db.Integer)
    hours_gaming = db.Column("hours_gaming",db.Integer)
    hours_productive = db.Column("hours_productive",db.Integer)
    
class ReceiptsShared(db.Model):
    """
    Keeps track of receipt sharing/access.
    """
    author_id = db.Column("author_id",db.Integer,db.ForeignKey(User.id))
    receiver_id = db.Column("receiver_id",db.Integer,db.ForeignKey(User.id))
    receipt_id = db.Column("author_id",db.Integer,db.ForeignKey(Receipts.receipt_id))

