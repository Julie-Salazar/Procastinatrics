
from app import app, db
from app.database import *



with app.app_context():

    print("Adding users") 
    AddUser("zac", "morris", "zac123", "password1234", "1")
    AddUser("james", "brown", "user43", "password1234", "1")
    AddUser("andy", "white", "user22", "password1234", "1")