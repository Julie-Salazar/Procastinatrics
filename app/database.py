
import flask

from app import app
from app import db
from app.models.user import User

# AddUser adds a User() entry to the database, must have all arguements
def AddUser(first_name, last_name, email, passwordHash, usertype):

    try:
        # passwordHash has not been hashed yet so it is nullified
        UserEntry = User(
            first_name   = first_name,
            last_name    = last_name,
            email    = email,
            passwordHash = "",
            usertype    = usertype)

        # convert the plaintext user inputted passwordHash into a hash 
        UserEntry.set_password(passwordHash)
        
        # add
        db.session.add(UserEntry) 

        # save   
        db.session.commit()             
    

    # handle database errors
    except InterruptedError as e:
        # rollback will make the database go back to original 
        db.sessions.rollback()
        print(f'An error occurred: {e}')    

# GetUser returns the database row for a specified user
# arguements:
# all are optional but you must specify at least one. You can query by uid and email
def GetUser(uid = None, email = None, usertype = None):

    query = db.session.query(User)
    
    # handle the optional arguements, only one can be used 
    if uid is not None:
        query = query.filter(User.uid == uid)
    elif email is not None:
        query = query.filter(User.email == email)
    elif usertype is not None:
        query = query.filter(User.usertype == usertype)
    else:
        # no parameters were supplied.
        print("You did not submit a parameter to use so returning all user records")

    # this converts from an array to a usable value, (the query should only have one value)
    user_record = query.first()
    
    return user_record