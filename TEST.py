
from app import app, db
from app.database import *


# adds 3 users to the database so testing can be done
#-----------------------------------------------------
# run with:
# python -m TEST

with app.app_context():

    print("Adding users") 
    AddUser("zac", "morris", "a@gmail.com", "password1234", "1")
    AddUser("james", "brown", "b@gmail.com", "password1234", "1")
    AddUser("andy", "white", "c@gmail.com", "password1234", "1")