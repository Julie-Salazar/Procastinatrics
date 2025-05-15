from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

# Import extensions and models
from app.models import db, login
from app.models.user import User
from app.models.activitylog import ActivityLog

# Create app instance
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login.init_app(app)
login.login_view = '/login'  # make sure this matches your actual login route
migrate = Migrate(app, db)

# Set up Flask-Admin
admin = Admin(app, name="Admin Panel", template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(ActivityLog, db.session))

# Import models-related views (like SQL view creators)
from app.models import views as model_views

# Register routes (Blueprints)
from app.routes.analytics_route import views
from app.routes.login_route import auth
from app.routes.log_route import log
from app.routes.share_route import share
from app.routes.friend_route import friends
from app.routes.receipts_route import receipts
# from app.routes.profile_settings_route import settings  # if needed

#default route
from app.routes.default import default

app.register_blueprint(views)
app.register_blueprint(auth)
app.register_blueprint(log)
app.register_blueprint(share)
app.register_blueprint(friends)
app.register_blueprint(receipts)

# app.register_blueprint(settings)

# Application context setup
with app.app_context():
    db.create_all()
    model_views.init()  # setup custom SQL views
