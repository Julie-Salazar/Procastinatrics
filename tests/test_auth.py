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
    rv = client.post("/login", data={"email":"no@one","password":"xxx"}, follow_redirects=True)
    assert rv.status_code == 200
    assert b"Log In" in rv.data

def test_login_and_access_protected(client):
    # create and login a real user
    AddUser("A","B","a@b.com","secret123","tester")
    rv = client.post("/login",
                     data={"email":"a@b.com","password":"secret123"},
                     follow_redirects=True)
    # after login you land on analytics-home
    assert rv.status_code == 200
    assert b"Dashboard" in rv.data

    # now protected route
    rv2 = client.get("/share")
    assert rv2.status_code == 200
    assert b"Share your shame" in rv2.data  # from share.html’s <h1>