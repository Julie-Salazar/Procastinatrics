from app.database import AddUser, GetUser
from app.models.user import User

def test_add_and_get_user(client):
    # add a user
    AddUser("Test","User","test@uwa.edu.au","p@ssw0rd","tester")
    # fetch by email
    u = GetUser(email="test@uwa.edu.au")
    assert isinstance(u, User)
    assert u.email == "test@uwa.edu.au"
    assert u.is_password_correct("p@ssw0rd")

    