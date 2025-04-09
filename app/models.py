from typing import List, Optional
from datetime import date, time
from sqlalchemy import ForeignKey, Column, Table, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app import db
from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    usertype = db.Column(db.String(20))
    passwordHash = db.Column(db.String(20))

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.passwordHash, password_plaintext)

    def set_password(self, plaintext: str):
        self.passwordHash = generate_password_hash(plaintext)

    