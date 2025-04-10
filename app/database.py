
import flask
from app import app
from app import db
from .models import *


def AddUser(first_name, last_name, user_name, passwordHash, usertype):

    try:
        UserEntry = User(
            first_name   = first_name,
            last_name    = last_name,
            user_name    = user_name,
            passwordHash = "",
            usertype    = usertype)

        UserEntry.set_password(passwordHash)
        
        db.session.add(UserEntry)    # add the changes 
        db.session.commit()             # save the changes
    
    except InterruptedError as e:
        db.sessions.rollback()
        print(f'An error occurred: {e}')    

def GetUser(uid = None, user_name = None, usertype = None):

    query = db.session.query(User)
    
    # handle the optional arguements, only one can be used 
    if uid is not None:
        query = query.filter(User.uid == uid)
    elif user_name is not None:
        query = query.filter(User.user_name == user_name)
    elif usertype is not None:
        query = query.filter(User.usertype == usertype)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all user records")

    
    attendance_records = query.first()
    
    return attendance_records