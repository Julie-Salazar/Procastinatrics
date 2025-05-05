from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Import extensions
from app.models import db, login
from app.models.user import User
from app.models.activitylog import ActivityLog

# Create the flask app instance
app = Flask(__name__)
app.config.from_object(Config)

# Init extensions
db.init_app(app)
login.init_app(app)
login.login_view = '/login'
migrate = Migrate(app, db)

# Admin panel
admin = Admin(app, name="Admin Panel", template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(ActivityLog, db.session))

# Import routes and views only after app/init setup
from app import routes
from app.models import views

# Wrap context-dependent setup
with app.app_context():
    db.create_all()
    views.init()
