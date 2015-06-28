from flask import Flask, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

app = Flask(__name__)  # Assign the Flask App to the `app` variable.
app.config.from_object("config")  # Load the configuration from `config.py`.

db = SQLAlchemy(app)  # Assign the database to the Flask App.

login_manager = LoginManager()  # Assign the Flask-Login Manager to the `login_manager` variable.
login_manager.init_app(app)  # Assign the Login Manager to the Flask App.
login_manager.login_view = "auth.login"  # Where to send unauthenticated users to login.


@login_manager.user_loader
def load_user(username):
    """Gives Flask-Login the current users object."""
    return db.session.query(forms.Runner).get(username)


@app.before_request
def before_request():
    """Gives Flask the current users object."""
    g.user = current_user

from app import models, password, forms  # Import files used within the application.

# Load all the Flask blueprints into the Flask App.

from app.home.views import home
app.register_blueprint(home)  # Homepages

from app.auth.views import auth
app.register_blueprint(auth)  # Login/Register

from app.webapp.views import webapp
app.register_blueprint(webapp, url_prefix="/app")  # Runner App

from app.admin.views import admin
app.register_blueprint(admin, url_prefix="/app/admin")  # Organiser App