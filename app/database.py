
import flask
from app import app
from app import db
from .models import *



def GetUser(uid = None, usertype = None):

    query = db.session.query(User)
    
    # handle the optional arguements, only one can be used 
    if uid is not None:
        query = query.filter(User.uid == uid)
    elif usertype is not None:
        query = query.filter(User.usertype == usertype)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all user records")

    
    attendance_records = query.first()
    
    return attendance_records