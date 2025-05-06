import pytest
from app import app, db
from app.database import User

@pytest.fixture
def client():
    # use in-memory DB and disable CSRF for forms
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
    )
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            test_user = User(email="rex@orange.com", first_name="Alex", last_name="O'Connor", usertype="tester")
            test_user.set_password("Apr!cotPr!nc355")
        yield client
        with app.app_context():
            db.drop_all()