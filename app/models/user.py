from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, login

class User(db.Model, UserMixin):
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    usertype = db.Column(db.String(20))
    passwordHash = db.Column(db.String(128))

    @property
    def id(self):
        return self.uid

    def is_password_correct(self, password_plaintext: str):
        return check_password_hash(self.passwordHash, password_plaintext)

    def set_password(self, plaintext: str):
        self.passwordHash = generate_password_hash(plaintext)

@login.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))
