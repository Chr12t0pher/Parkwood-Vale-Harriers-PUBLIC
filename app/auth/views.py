from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from app import forms, models, db, password


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    registration = forms.RegistrationForm()
    if registration.validate_on_submit():
        password_table = password.hash_password(registration.confirm.data)  # Generates a secure hashed password.
        registration.confirm.data = None  # Removes the users password from the memory.
        new = models.Runner(username=registration.username.data,
                            email=registration.email.data,
                            name=registration.name.data,
                            phone_number=registration.phone_number.data,
                            address=registration.address.data,
                            town=registration.town.data,
                            county=registration.county.data,
                            postcode=registration.postcode.data,
                            gender=registration.gender.data,
                            date_of_birth=registration.date_of_birth.data,
                            hashed_password=password_table[0],
                            salt=password_table[1])
        db.session.add(new)
        db.session.commit()
        flash("Account created, please login!", "success")
        return redirect(url_for("auth.login"))
    else:
        return render_template("pages/register.html", form=registration)


@auth.route("/validate/<username>")
def validate_user(username):
    user = models.Runner.query.filter_by(username=username).first()
    user.verified = True
    db.session.add(user)
    db.session.commit()
    return redirect(url_for("auth.login"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = forms.LoginForm()
    if current_user.is_authenticated():
        return redirect(url_for("app_home"))  # Sends user to the webapp if they are already logged in.
    elif login_form.validate_on_submit():
        login_user(login_form.get_user(), remember=login_form.remember_me.data)
        flash("Successfully logged in.", "success")
        return redirect(url_for("webapp.home"))
    else:
        return render_template("pages/login.html", form=login_form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out.", "success")
    return redirect(url_for("home.homepage"))