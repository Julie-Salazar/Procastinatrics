from .login_route import *
from .analytics_route import *
from .share_route import *
from .friend_route import *
from .log_route import *


from flask import Flask

# Create flask app instance
app = Flask(__name__)

from app.routes import analytics_route, profile_settings_route, share_route, friend_route, log_route

app.config['SECRET_KEY'] = 'your-secret-key'

