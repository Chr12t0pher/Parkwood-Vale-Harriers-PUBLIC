from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
from app import forms, models, db
from app.functions import admin_required

admin = Blueprint("admin", __name__)


@admin.route("/")
@login_required
@admin_required
def home():
    return render_template("pages/admin/admin.html", user=current_user)


@admin.route("/viewtraining")
@login_required
@admin_required
def view_training():
    return render_template("pages/admin/viewtraining.html", user=current_user,
                           training=models.Training.query.order_by(models.Training.date.desc()).all())


@admin.route("/viewusers")
@login_required
@admin_required
def view_users():
    return render_template("pages/admin/viewusers.html", user=current_user,
                           users=models.Runner.query.order_by(models.Runner.id).all())


@admin.route("/chooserunners")
@login_required
@admin_required
def choose_runners():
    runner_data = {}
    ranking_data = {}
    ranked_runners = []
    for runner in models.Runner.query.all():
        # For each runner, create a simple data structure.
        runner_data[runner.username] = {"name": runner.name,
                                        "username": runner.username,
                                        "email": runner.email,
                                        "phone_number": runner.phone_number,
                                        "training_calories": {"running": 0,
                                                              "cycling": 0,
                                                              "swimming": 0},
                                        "training_calories_": 0,
                                        "training_distance": 0,
                                        "training_hours": 0,
                                        "training_rank": {"running": 0,
                                                          "cycling": 0,
                                                          "swimming": 0},
                                        "rank": 0}
    for training in models.Training.query.all():
        # For each training entry in the database, add the calories burnt to the relevant category
        runner_data[training.username]["training_calories"][training.training_type] += training.calories_burnt
        runner_data[training.username]["training_calories_"] += training.calories_burnt
        runner_data[training.username]["training_distance"] += training.distance
        runner_data[training.username]["training_hours"] += training.hours_trained
    for training_type in ["running", "cycling", "swimming"]:
        # Create a list for each training type ordered by the runner with the most calories burnt.
        ranking_data[training_type] = sorted(runner_data,
                                             key=lambda x: runner_data[x]["training_calories"][training_type],
                                             reverse=True)
    for runner in runner_data:
        # For each runner, set their rank in each training category. Adding 1 because lists start at 0.
        for training_type in ["running", "cycling", "swimming"]:
            runner_data[runner]["training_rank"][training_type] = \
                ranking_data[training_type].index(runner) + 1
        # Generate runners overall rank by averaging their three rankings.
        runner_data[runner]["rank"] = sum(runner_data[runner]["training_rank"].values()) / 3

    user_ranking = sorted(runner_data, key=lambda x: runner_data[x]["rank"])  # Sort the runners by overall rank.
    for username in user_ranking:
        # Add the runner dictionaries in order to the final list.
        ranked_runners.append(runner_data[username])
    return render_template("pages/admin/chooserunners.html", user=current_user, runners=ranked_runners)