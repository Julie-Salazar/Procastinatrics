import flask

from app import app
from .database import *

from .models import *

import os
from datetime import datetime, date
import sqlalchemy as sa
import pandas as pd



@app.route("/login")
def index():

    # for front end change (uid = 1) to the form input box data : eg user types in password '1234' (uid = form.password)
    user = GetUser(user_name='zac123')
    

    if user is None:
        # username is not found
        return "username not found"
    
    if user.is_password_correct("password1234") == False:
        return "Password is incorrect"
    
    

    # below for the front end change to (return login.html)
    return "logged in as " + user.first_name + " " + user.last_name + " with password " + user.passwordHash