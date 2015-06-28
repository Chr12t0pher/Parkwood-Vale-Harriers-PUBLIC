from app.models import Training, Runner
from functools import wraps
from app import current_user
from flask import Response


def homepage_progress(current_user):
    """Generates the percentage width of the progress bars on the Web App homepage.
    :param current_user: The object of the user requesting the progress bars.
    :returns: A dictionary containing both the leader and the users progress percentages."""
    def add_up_distance(training_type, username):
        data = 0
        x = Training.query.filter_by(training_type=training_type, username=username).all()
        for i in x:
            data += i.distance
        return data

    def add_calories(username):
        data = 0
        for i in Training.query.filter_by(username=username).all():
            data += i.calories_burnt
        return data

    def top_distance(training_type):
        data = 0
        for user in Runner.query.order_by(Runner.username):
            x = add_up_distance(training_type, user.username)
            if x > data:
                data = x
        return data

    def top_calories():
        data = 0
        for user in Runner.query.order_by(Runner.username):
            x = add_calories(user.username)
            if x > data:
                data = x
        return data

    def calculate_percentage(top, user):
        if user == 0:
            return 10
        percent = (((user - top) / top) * 90)
        if percent < 0:
            percent *= -1
        if percent <= 10:
            return 10
        else:
            return percent
    percentages = {"calories": calculate_percentage(top_calories(), add_calories(current_user.username)),
                   "running": calculate_percentage(top_distance("running"), add_up_distance("running",
                                                                                            current_user.username)),
                   "cycling": calculate_percentage(top_distance("cycling"), add_up_distance("cycling",
                                                                                            current_user.username)),
                   "swimming": calculate_percentage(top_distance("swimming"), add_up_distance("swimming",
                                                                                              current_user.username))}
    return percentages


def admin_required(func):
    """Custom function that checks if the user is an Admin. Based off of the standard Flask-Login @login_required.
    :returns: Continues if Admin, else returns 401.
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if current_user.admin is True:
            return func(*args, **kwargs)
        elif current_user.admin is None or current_user.admin is False:
            return Response("You are not permitted to access this page!", 401)
        return func(*args, **kwargs)
    return decorated_view
