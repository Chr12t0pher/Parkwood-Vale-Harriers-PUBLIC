from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app.training_math import *
from app.functions import homepage_progress
from app import forms, models, db
from app.models import Training

webapp = Blueprint("webapp", __name__)

training_errors = {}
details_errors = {}

@webapp.route("/")
@login_required
def home():
    return render_template("pages/webapp/app.html", user=current_user, percentages=homepage_progress(current_user))



@webapp.route("/training")
@login_required
def training():
    return render_template("pages/webapp/training.html", user=current_user)


@webapp.route("/addtraining")
@login_required
def add_training():
    global training_errors
    running = forms.RunTraining()
    cycling = forms.CycleTraining()
    swimming = forms.SwimTraining()
    for i in training_errors:
        for x in training_errors[i]:
            flash(training_errors[i][x][0], "danger")
    training_errors = {}
    return render_template("pages/webapp/addtraining.html", user=current_user, running=running,
                           cycling=cycling, swim=swimming)


@webapp.route("/addtraining/running", methods=["POST"])
@login_required
def add_training_running():
    running = forms.RunTraining()
    global training_errors
    if running.validate_on_submit():
        new = models.Training(username=current_user.username,
                              date=running.date.data,
                              training_type="running",
                              hours_trained=running.hours_trained.data,
                              calories_burnt=calculate_running(running.speed.data, running.hours_trained.data),
                              distance=running.distance.data)
        db.session.add(new)
        db.session.commit()
        flash("Running session added to your profile!", "success")
    elif running.errors != {}:
        training_errors["running"] = running.errors
    return redirect(url_for("webapp.add_training"))


@webapp.route("/addtraining/cycling", methods=["POST"])
@login_required
def add_training_cycling():
    cycling = forms.CycleTraining()
    global training_errors
    if cycling.validate_on_submit():
        new = models.Training(username=current_user.username,
                              date=cycling.date.data,
                              training_type="cycling",
                              hours_trained=cycling.hours_trained.data,
                              calories_burnt=calculate_cycling(cycling.speed.data, cycling.hours_trained.data),
                              distance=cycling.distance.data)
        db.session.add(new)
        db.session.commit()
        flash("Cycling session added to your profile!", "success")
    elif cycling.errors != {}:
        training_errors["cycling"] = cycling.errors
    return redirect(url_for("webapp.add_training"))


@webapp.route("/addtraining/swimming", methods=["POST"])
@login_required
def add_training_swimming():
    swimming = forms.SwimTraining()
    global training_errors
    if swimming.validate_on_submit():
        new = models.Training(username=current_user.username,
                              date=swimming.date.data,
                              training_type="swimming",
                              hours_trained=swimming.hours_trained.data,
                              calories_burnt=calculate_swimming(swimming.stroke.data, swimming.hours_trained.data),
                              distance=swimming.distance.data)
        db.session.add(new)
        db.session.commit()
        flash("Swimming session added to your profile!", "success")
    elif swimming.errors != {}:
        training_errors["swimming"] = swimming.errors
    return redirect(url_for("webapp.add_training"))


@webapp.route("/viewtraining")
@login_required
def view_training():
    return render_template("pages/webapp/viewtraining.html", user=current_user,
                           training=Training.query.filter_by(
                               username=current_user.username).order_by(Training.date.desc()).all())


@webapp.route("/viewtraining/remove/<identifier>")
@login_required
def remove_training(identifier):
    queriedid = models.Training.query.filter_by(username=current_user.username, id=identifier).first()
    if queriedid is not None:
        db.session.delete(queriedid)
        db.session.commit()
        flash("Training removed successfully!", "success")
        return redirect(url_for("webapp.view_training"))
    else:
        flash("You didn't do that training, you cannot remove it!", "danger")
        return redirect(url_for("webapp.view_training"))


@webapp.route("/user/<username>")
@login_required
def user(username):
    return render_template("pages/webapp/user.html", user=current_user,
                           requested_user=models.Runner.query.filter_by(username=username).first())


@webapp.route("/user/edit", methods=["GET", "POST"])
@login_required
def user_edit():
    global details_errors
    details = forms.UserEditForm()
    settings = forms.UserSettingsForm()
    for i in details_errors:
        flash(details_errors[i][0], "danger")
    details_errors = {}
    return render_template("pages/webapp/useredit.html", user=current_user, userform=details, settingsform=settings)


@webapp.route("/user/updateuser", methods=["POST"])
@login_required
def user_update_user():
    details = forms.UserEditForm()
    global details_errors
    if details.validate_on_submit():
        user = models.Runner.query.filter_by(username=current_user.username).first()
        ignore = ["salt", "hashed_password", "messages", "id", "verified", "admin"]
        for variable in [attr for attr in vars(user) if not callable(attr) and
                         not attr.startswith("_") and attr not in ignore]:
            if getattr(details, variable).data != getattr(user, variable) and getattr(details, variable).data != "":
                setattr(user, variable, getattr(details, variable).data)
        db.session.add(user)
        db.session.commit()
        flash("Your details have been amended!", "success")
    elif details.errors != {}:
        details_errors = details.errors
    return redirect(url_for("webapp.user_edit"))


@webapp.route("/user/updatesettings", methods=["POST"])
@login_required
def user_update_settings():  # TODO - Create settings field in database for users. Don't use, will probably break.
    settings = forms.UserEditForm()
    if settings.validate_on_submit():
        user = models.Runner.query.filter_by(username=current_user.username).first()
        ignore = ["salt", "hashed_password", "messages", "id"]
        for variable in [attr for attr in vars(user) if not callable(attr) and
                         not attr.startswith("_") and attr not in ignore]:
            if getattr(settings, variable).data != getattr(user, variable):
                setattr(user, variable, getattr(settings, variable).data)
                print(getattr(user, variable))
        db.session.add(user)
        db.session.commit()
        flash("Your details have been amended!", "success")