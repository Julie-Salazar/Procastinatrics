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
    p = GetUser(uid='1')
    
    return p.first_name