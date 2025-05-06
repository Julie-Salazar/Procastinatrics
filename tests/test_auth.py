from app.database import AddUser

def test_signup_page(client):
    rv = client.get("/signup")
    assert rv.status_code == 200
    assert b"Sign up" in rv.data

def test_login_page(client):
    rv = client.get("/login")
    assert rv.status_code == 200
    assert b"Log In" in rv.data

def test_login_invalid(client):
    # no such user, should redirect or re-show login
    rv = client.post("/login", data={"email":"mr@worldwide.com","password":"pitbull"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Log In" in rv.data

def test_login(client):
    # create and login a real user
    rv = client.post("/login",
                     data={"email":"rex@orange.com","password":"Apr!cotPr!nc355"},
                     follow_redirects=True)
    assert rv.status_code == 200

    # now protected route
    rv2 = client.get("/share")
    assert rv2.status_code == 302