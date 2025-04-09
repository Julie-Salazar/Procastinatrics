from typing import List, Optional
from datetime import date, time
from sqlalchemy import ForeignKey, Column, Table, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app import db
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    usertype = db.Column(db.String(20))

    