from app import db
from app.models.base import BaseModel

class Status:
    ACCEPTED = 'Accepted'
    IGNORED = 'Ignored'
    PENDING = 'Pending'
    DECLINED = 'Declined'
    BLOCKED = 'Blocked'
    
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
    

class ReceiptsShareRequest(BaseModel):
    request_id = db.Column("request_id", db.Integer, primary_key=True)
    sender_id = db.Column("sender_id", db.Integer, db.ForeignKey("user.uid"))
    receiver_id = db.Column("receiver_id", db.Integer, db.ForeignKey("user.uid"))
    shared_receipt_id = db.Column("shared_receipt_id", db.Integer, db.ForeignKey("receipts.receipt_id"))
    status = db.Column("status",db.String(20))
    time = db.Column("time",db.Integer)
    
class BlockedUsers(BaseModel):
    __tablename__ = 'blocked_users'
    id = db.Column("id", db.Integer, primary_key=True)
    blocker_id = db.Column("blocker_id", db.Integer, db.ForeignKey("user.uid"))
    target_user_id = db.Column("target_user_id", db.Integer, db.ForeignKey("user.uid"))
    
