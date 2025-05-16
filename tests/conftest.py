import pytest
from app import app, db
from app.database import User
from app.models.activitylog import ActivityLog

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
            db.drop_all()
            db.create_all()
            test_user = User(first_name='test',
                             last_name='user',
                             email='test@example.com')
            test_user.set_password('password')
            db.session.add(test_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture
def client_logged(client):
    client.post('/login', data={'email':'test@example.com',
                                'password':'password'})
    return client