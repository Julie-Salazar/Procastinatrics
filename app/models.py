from typing import List, Optional
from datetime import date, time
from sqlalchemy import ForeignKey, Column, Table, Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app import db, login
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    usertype = db.Column(db.String(20))
    passwordHash = db.Column(db.String(20))

    @property
    def id(self):
        return self.uid

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.passwordHash, password_plaintext)

    def set_password(self, plaintext: str):
        self.passwordHash = generate_password_hash(plaintext)



@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

    