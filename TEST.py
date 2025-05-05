
from app import app, db
from app.database import *
from app.models.user import User
from app.models.activitylog import ActivityLog
from app.models import views

# adds 3 users to the database so testing can be done
#-----------------------------------------------------
# run with:
# python -m TEST

from sqlalchemy import text

def test_database():
    db.drop_all()
    db.create_all()
    test_user = User(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        usertype="tester"
    )
    test_user2 = User(
        email="albo@labor.com",
        first_name="Anthony",
        last_name="Albanese",
        usertype="albo"
    )
    test_user.set_password("password")
    test_user2.set_password("password!")
    db.session.add_all([test_user,test_user2])
    db.session.commit()
    
    # Add some Mood records for the test user
    mood1 = Mood(
        author_id=test_user.uid,
        app_name="Netflix",
        app_type="procrastination",
        minutes_spent=60,
        mood_emoji="😴"
    )
    mood2 = Mood(
        author_id=test_user.uid,
        app_name="Steam",
        app_type="gaming",
        minutes_spent=120,
        mood_emoji="😀"
    )
    mood3 = Mood(
        author_id=test_user.uid,
        app_name="VSCode",
        app_type="productive",
        minutes_spent=30,
        mood_emoji="💻"
    )
    
    mood2_1 = Mood(
        author_id=test_user2.uid,
        app_name="Tetr.io",
        app_type="gaming",
        minutes_spent=240,
        mood_emoji="😀"
    )
    
    mood2_2 = Mood(
        author_id=test_user2.uid,
        app_name="csmarks",
        app_type="productive",
        minutes_spent=1,
        mood_emoji="😀"
    )
    
    db.session.add_all([mood1, mood2, mood3,mood2_1,mood2_2])
    db.session.commit()

    # Reinitialize the Hours view (this creates/updates the view defined in views.py)
    views.create_hours_view()

    # Query the Hours view using a raw SQL statement
    with db.engine.connect() as connection:
        result = connection.execute(text("SELECT * FROM hours")).fetchall()
        print("Hours view results:")
        for row in result:
             print(dict(row._mapping))
    print()
        
def test_users():
    users = User.query.all()
    print("Users in database:")
    for user in users:
        print({
            'uid': user.uid,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'usertype': user.usertype
        })
with app.app_context():

    print("Adding users") 
    AddUser("zac", "morris", "a@gmail.com", "password1234", "1")
    AddUser("james", "brown", "b@gmail.com", "password1234", "1")
    AddUser("andy", "white", "c@gmail.com", "password1234", "1")
    test_users()
    test_database()
    