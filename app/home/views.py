from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user


home = Blueprint("home", __name__)


@home.route("/")
@home.route("/home")
def homepage():
    return render_template("pages/homepage.html", user=current_user)


@home.route("/documentation")
def documentation():
    return render_template("pages/documentation.html")