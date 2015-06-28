"""
Makes the specified user an Admin so they can log into the Admin/Organiser Panel.
"""

from app import db
from app.models import Runner

username = input("Username: ")
userobject = Runner.query.filter_by(username=username).first()

if userobject is None:
    exit("Not a valid Username")
userobject.admin = True

db.session.add(userobject)
db.session.commit()