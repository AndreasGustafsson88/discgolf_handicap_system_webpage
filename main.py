from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required, logout_user
from werkzeug.utils import secure_filename
from models import User
import os
from models import UploadForm
from settings import *
from settings.functions import read_csv
import pickle

main = Blueprint("main", __name__)


@main.context_processor
def load_user():
    return dict(mydict=current_user.name)


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@main.route("/stats")
@login_required
def stats():

    if current_user.score_card != "none":

        try:
            score = read_csv(current_user.score_card, current_user.udisc_name)
            if score == {}:
                msg = f"Woops, looks like no scores could be found. Check if '{current_user.udisc_name}' is correct " \
                      f"username or that the scorecard was uploaded correct"
                return render_template("stats.html", msg=msg)
            return render_template("stats.html", iterable=score)

        except ValueError:
            msg = f"Seems like the username entered was incorrect, check if '{current_user.udisc_name}' is correct"
            return render_template("stats.html", msg=msg)

    msg = "No scorecard could be found, please upload score card and enter Udisc username to see player stats"
    return render_template("stats.html", msg=msg)


@main.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    form = UploadForm()

    if form.validate_on_submit():
        f = form.file.data
        file_name = secure_filename(f.filename)
        f.save(os.path.join(UPLOAD_FOLDER, file_name))
        current_user.score_card = os.path.join(UPLOAD_FOLDER, file_name)
        flash("File uploaded successfully")

        udisc_name = request.form.get("udisc")
        current_user.udisc_name = udisc_name

        db.session.commit()

        return redirect(url_for("main.stats"))

    return render_template("upload.html", form=form)


@main.route("/courses")
@login_required
def courses():
    return render_template("courses.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("auth.index"))

