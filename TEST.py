
from app import app, db
from app.database import *
from app.models.user import User
from app.models.activitylog import ActivityLog
from app.models.receipts import Receipts,ReceiptsShareRequest,Status
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
    mood1 = ActivityLog(
        user_id=test_user.uid,
        application="Netflix",
        category="procrastination",
        hours=0,
        minutes=60,
        mood="😴",
        timestamp=db.func.current_timestamp()
    )
    mood2 = ActivityLog(
        user_id=test_user.uid,
        application="Steam",
        category="gaming",
        hours=2,
        minutes=0,
        mood="😀",
        timestamp=db.func.current_timestamp()
    )
    mood3 = ActivityLog(
        user_id=test_user.uid,
        application="VSCode",
        category="productive",
        hours=0,
        minutes=30,
        mood="💻",
        timestamp=db.func.current_timestamp()
    )
    
    mood2_1 = ActivityLog(
        user_id=test_user2.uid,
        application="Tetr.io",
        category="gaming",
        hours=3,
        minutes=0,
        mood="😀",
        timestamp=db.func.current_timestamp()
    )
    
    mood2_2 = ActivityLog(
        user_id=test_user2.uid,
        application="csmarks",
        category="productive",
        hours=0,
        minutes=1,
        mood="😀",
        timestamp=db.func.current_timestamp()
    )
    receipt = Receipts(
        author_id = test_user2.uid,
        time = db.func.current_timestamp(),
        hours_procrastinated = 70,
        hours_gaming = 80,
        hours_productive = 99
    )
    receipt_request = ReceiptsShareRequest(
        sender_id = test_user2.uid,
        receiver_id = test_user.uid,
        shared_receipt_id = receipt.receipt_id,
        status = Status.PENDING,
        time = db.func.current_timestamp()
    )
    db.session.add_all([mood1, mood2, mood3,mood2_1,mood2_2,receipt,receipt_request])
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
    