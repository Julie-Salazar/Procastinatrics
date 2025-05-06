from app.database import AddUser, GetUser
from app.models.user import User
from app import db
from sqlalchemy import select

def test_add_and_get_user(client):
    # TODO: add a user through signup
    assert True
    added = User(first_name="Test",last_name="User",email="test@uwa.edu.au",usertype="tester")
    added.set_password("p@ssw0rd")
    
    # TODO: query database for the user
    #assert isinstance(user, User)
    #assert user.email == "test@uwa.edu.au"
    #assert user.is_password_correct("p@ssw0rd")

    