import os

WTF_CSRF_ENABLED = True
SECRET_KEY = "8a7c5c62e3dd7ba27aa280e8d37055e5953ca35881883875c83810b791dc533c"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, "db_repository")