from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_required, logout_user
from werkzeug.utils import secure_filename
from models import User
import os
from models import UploadForm
from settings import *
from settings.data_functions.get_ext_data import download
from settings.functions import read_csv, list_courses, sort_rounds, calc_rating

main = Blueprint("main", __name__)


@main.context_processor
def load_user():
    return dict(mydict=current_user.name)


@main.route("/profile")
@login_required
def profile():
    return render_template("new/profile.html")


@main.route("/stats")
@login_required
def stats():

    if current_user.score_card != "none":
        try:
            score = read_csv(current_user.score_card, current_user.udisc_name)
            player_score = sort_rounds(current_user.score_card, current_user.udisc_name)
            if score == {}:
                msg = f"Woops, looks like no scores could be found. Check if '{current_user.udisc_name}' is correct " \
                      f"username or that the scorecard was uploaded correct"
                return render_template("new/stats.html", msg=msg)
            player_rating, rounds = calc_rating(player_score)
            current_user.udisc_rating = player_rating
            db.session.commit()

            return render_template("new/stats.html", iterable=score, rating=player_rating, rounds=rounds)

        except ValueError:
            msg = f"Seems like the username entered was incorrect, check if '{current_user.udisc_name}' is correct"
            return render_template("new/stats.html", msg=msg)

    msg = "No scorecard could be found, please upload score card and enter Udisc username to see player stats"
    return render_template("new/stats.html", msg=msg)


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

    if request.method == "POST":
        if "pdga" in request.form:
            pdga = str(request.form.get("pdga"))
            current_user.pdga_rating = download(pdga, pdga=True)
            db.session.commit()
            flash(f"PDGA-rating {current_user.pdga_rating} saved!")
            return redirect(request.url)

        if "metrix" in request.form:
            metrix = request.form.get("metrix")
            current_user.metrix_rating = metrix
            db.session.commit()
            flash(f"Metrix-rating {current_user.metrix_rating} saved")
            return redirect(request.url)

    return render_template("new/upload.html", form=form)


@main.route("/courses")
@login_required
def courses():
    all_courses = list_courses()
    return render_template("new/courses.html", courses=all_courses)


@main.route("/go_play", methods=["POST", "GET"])
@login_required
def go_play():
    try:
        if request.method == "POST":
            course = request.form.get("course")
            holes, par, difference = main_db.get_throws(current_user.metrix_rating, course)
            return render_template("new/go_play.html",  holes=holes, par=par, course=course, difference=difference)
    except IndexError:
        flash("You have not submittet a valid scorecard. Could not find any rating information about you!")
        return redirect(url_for("main.go_play"))
    return render_template("new/go_play.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.index"))

