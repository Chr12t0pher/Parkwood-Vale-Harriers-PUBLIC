from app import db
from datetime import date


class Runner(db.Model):
    """Database storing all the Runners and their details."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    phone_number = db.Column(db.Integer)
    address = db.Column(db.String)
    town = db.Column(db.String)
    county = db.Column(db.String)
    postcode = db.Column(db.String)
    gender = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    hashed_password = db.Column(db.String)
    salt = db.Column(db.String)
    verified = db.Column(db.Boolean)
    admin = db.Column(db.Boolean)

    training = db.relationship("Training", backref="training", lazy="dynamic")  # Link Runners Training to Runner

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.verified

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return self.username

    # Custom Functions:
    def get_first_name(self):
        """Returns first word of users name."""
        return self.name.split(" ", 1)[0]

    def get_age(self):
        """Calculates age of user."""
        today = date.today()
        birthday = self.date_of_birth.split("/")
        birthday = [int(i) for i in birthday]
        return today.year - birthday[0] - ((today.month, today.day) < (birthday[1], birthday[2]))


class Training(db.Model):
    """Database storing the training for all users."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey("runner.username"))  # Use Runner Username as an identifier.
    date = db.Column(db.String)
    training_type = db.Column(db.String)
    hours_trained = db.Column(db.Integer)
    calories_burnt = db.Column(db.Integer)
    distance = db.Column(db.Integer)