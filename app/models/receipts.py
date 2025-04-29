from app import db
from . import User,BaseModel

class Receipts(BaseModel):
    """
    Stores data instead of accessing other tables.
    """
    receipt_id = db.Column("receipt_id",db.Integer,primary_key=True)
    author_id = db.Column("author_id",db.Integer,db.ForeignKey("user.uid"))
    time = db.Column("time",db.Integer)
    hours_procrastinated = db.Column("hours_procrastinated",db.Integer)
    hours_gaming = db.Column("hours_gaming",db.Integer)
    hours_productive = db.Column("hours_productive",db.Integer)
    
class ReceiptsShared(BaseModel):
    """
    Keeps track of receipt sharing/access.
    """
    share_id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column("author_id",db.Integer,db.ForeignKey("user.uid"))
    receiver_id = db.Column("receiver_id",db.Integer,db.ForeignKey("user.uid"))
    receipt_id = db.Column("receipt_id",db.Integer,db.ForeignKey("receipts.receipt_id"))

