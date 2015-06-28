from wtforms import StringField, PasswordField, IntegerField, DateField, RadioField, BooleanField, SelectField,\
    validators
from flask_wtf import Form
from app import current_user
from app.password import check_password
from app.models import Runner
from app import db, password


class RegistrationForm(Form):
    """
        Used on the /register page.
    """
    name = StringField("name")
    username = StringField("Username")
    email = StringField("Email")
    password = PasswordField("Password")
    confirm = PasswordField("Confirm Password")
    phone_number = IntegerField("Phone Number")
    address = StringField("Address")
    town = StringField("Town")
    county = StringField("County")
    postcode = StringField("Postcode")
    date_of_birth = DateField("Birthday", format="%d/%m/%Y")
    gender = RadioField("Gender", choices=[("M", "Male"), ("F", "Female")])

    def validate_username(self, field):
        """Checks if username is used in database already."""
        if Runner.query.filter_by(username=field.data).count() > 0:
            raise validators.ValidationError("Username In Use")

    def validate_email(self, field):
        """Checks if email is used in database already."""
        if Runner.query.filter_by(email=field.data).count() > 0:
            raise validators.ValidationError("Email in Use")
        else:
            # Validate user account by emailing them a link, when clicked allows them to login.
            # Could implement a mail server, but would be hard to ensure it works on moderators machines.
            print("Validate your account by going to http://127.0.0.1:5000/validate/" + self.username.data)


class LoginForm(Form):
    """
        Used on the /login page.
    """
    username = StringField("Username")
    password = PasswordField("Password")
    remember_me = BooleanField("RememberMe")

    def validate_password(self, field):
        """Checks if  both password entered matches the one stored in the database,
            and if the username entered exists."""
        if Runner.query.filter_by(username=self.username.data).count() == 0:
            # If username doesnt exist, raise an error.
            raise validators.ValidationError("Incorrect Username or Password")
        salt = Runner.query.filter_by(username=self.username.data).first().salt
        hashed_password = Runner.query.filter_by(username=self.username.data).first().hashed_password
        if password.check_password(field.data, salt, hashed_password) is not True:
            # If the hash generated from the provided password and stored salt for the username
            # doesnt match, raise an error.
            raise validators.ValidationError("Incorrect Username or Password")

    def get_user(self):
        """Return the user object for Flask-Login."""
        return db.session.query(Runner).filter_by(username=self.username.data).first()


class TrainingForm(Form):
    """
        Parent form for the following forms, used on the /app/addtraining page.
    """
    date = StringField()
    hours_trained = IntegerField()
    distance = IntegerField()


class RunTraining(TrainingForm):
    speed = IntegerField("Speed")

    def validate_speed(self, field):
        """Checks if the data the user entered is mathematically correct, and if the speed of their running is
            an acceptable speed."""
        if self.speed.data * self.hours_trained.data != self.distance.data:
            # If Speed x Hours Trained doesnt equal Distance, raise an error.
            raise validators.ValidationError("Check your maths, your numbers are wrong!")
        if self.speed.data > 12:
            # If the Speed is too fast, raise an error.
            raise validators.ValidationError("Are you sure your ran that fast?")


class CycleTraining(TrainingForm):
    speed = IntegerField("Speed")

    def validate_speed(self, field):
        """Checks if the data the user entered is mathematically correct, and if the speed of their cycling is
            an acceptable speed."""
        if self.speed.data * self.hours_trained.data != self.distance.data:
            # If Speed x Hours Trained doesnt equal Distance, raise an error.
            raise validators.ValidationError("Check your maths, your numbers are wrong!")
        if self.speed.data > 25:
            # If the Speed is too fast, raise an error.
            raise validators.ValidationError("Are you sure you cycled that fast?")


class SwimTraining(TrainingForm):
    stroke = SelectField("Stroke", choices=[("freestyle_slow", "Freestyle - Slow"),
                                            ("freestyle_fast", "Freestyle - Fast"), ("backstroke", "Backstroke"),
                                            ("breaststroke", "Breaststroke"), ("butterfly", "Butterfly")])


class UserEditForm(Form):
    """
        Used on the /app/user/edit page
    """
    name = StringField("name")
    username = StringField("Username")
    email = StringField("Email")
    oldpassword = PasswordField("Old Password")
    newpassword = PasswordField("New Password")
    confirm = PasswordField("Confirm Password")
    phone_number = StringField("Phone Number")
    address = StringField("Address")
    town = StringField("Town")
    county = StringField("County")
    postcode = StringField("Postcode")
    date_of_birth = StringField("Birthday")
    gender = RadioField("Gender", choices=[("M", "Male"), ("F", "Female")])

    def validate_oldpassword(self, field):
        """Checks if the users current password is correct."""
        if check_password(field.data, current_user.salt, current_user.hashed_password) is not True:
            raise validators.ValidationError("Incorrect Password")


class UserSettingsForm(Form):
    pass