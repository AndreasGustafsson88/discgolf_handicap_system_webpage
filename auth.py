from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from settings import db


auth = Blueprint('auth', __name__)


@auth.route("/")
@auth.route("/home")
def index():

    return render_template("new/index.html")


@auth.route("/signup")
def signup():
    return render_template("new/signup.html")


@auth.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()

    if user:
        flash("Email already exists")
        return redirect(url_for("auth.signup"))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method="sha256"))
    db.session.add(new_user)
    db.session.commit()

    flash("Registration successful!")

    return redirect(url_for("auth.login"))


@auth.route("/login")
def login():
    return render_template("new/login.html")


@auth.route("/login", methods=["POST"])
def login_post():

    email = request.form.get("email")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("Email incorrect")
        return redirect(url_for("auth.login"))

    if not check_password_hash(user.password, password):
        flash("Password incorrect")
        return redirect(url_for("auth.login"))

    login_user(user)
    return redirect(url_for("main.profile", remeber=remember))


@auth.route("/about")
def about():
    return "About"


