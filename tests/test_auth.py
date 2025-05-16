import pytest

#Page/Routing Functionality Tests
@pytest.mark.parametrize("protected_route", [
    pytest.param('/share', id="Share page"),
    pytest.param('/analytics-home', id="Analytics page"),
    pytest.param('/profile-settings', id="Profile page"),
])

def test_access_protected_routes(client, protected_route):
    response = client.get(protected_route)
    assert '/login' in response.location, f'Login protection error: did not redirect to /login!'

def test_access_login(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_signup_valid(client):
    client.get("signup")
    response = client.post("/signup", data={
        'email':'signup@test.com',
        'password':'password',
        'confirm':'password',
        'first_name':'Signup',
        'last_name':'Testing'
    })
    assert response.status_code == 302, f"Unexpected code: expected 302, got {response.status_code}"
    assert b'signup' not in response.data.lower()

def test_signup_invalid_duplicate_email(client):
    response = client.post("/signup", data={
        'email':'test@example.com',
        'password':'different_pwd',
        'first_name':'Shouldnt',
        'last_name':'Exist'
    })
    assert b'error' in response.data, "Expected error for invalid signup!"

def test_signup_invalid_no_password(client):
    response = client.post("/signup", data={
        'email':'signup@test.com',
        'password':'',
        'first_name':'Signup',
        'last_name':'Testing'
    })
    assert b'error' in response.data, "Expected error for invalid signup!"

def test_login_invalid(client):
    # no such user, should redirect or re-show login
    rv = client.post("/login", data={"email":"mr@worldwide.com","password":"pitbull"}, follow_redirects=True)
    assert rv.status_code == 200

def test_login(client):
    # create and login a real user
    rv = client.post("/login",
                     data={"email":"rex@orange.com","password":"Apr!cotPr!nc355"},
                     follow_redirects=True)
    assert rv.status_code == 200

    # now protected route
    rv2 = client.get("/share")
    assert rv2.status_code == 302