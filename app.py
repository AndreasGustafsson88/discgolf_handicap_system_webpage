from flask import Flask, render_template, request, flash, url_for, redirect
import os
from settings.data_functions import read_csv

UPLOAD_FOLDER = "C:\\Kod\\Projekt\\handikapp_webpage\\uploads"
ALLOWED_FORMAT = (".csv",)

app = Flask(__name__)
app.secret_key = "Hello"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

course = [
    "1: Gässlösa DGB Hole 1-18 (2020)",
    "2: Holmenkollen DiscGolfpark Normal Oppsett",
    "3: Krokhol Disc Golf Course Krokhol Regular Layout",
    "4: Stovner Discgolfpark Main",
    "5: Ymergårdens Discgolfcenter 2020 tournament layout"]


@app.route('/', methods=["POST", "GET"])
def home():
    error = None
    if request.method == "POST":
        user = request.form
        if user["username"] != "admin" or user["password"] != "admin":
            error = "Invalid credentials, please try again!"
        else:
            return redirect(url_for("upload", username=user["username"]))
    return render_template("home.html", error=error)


@app.route("/upload/<username>")
def upload(username):
    flash("Login successful")
    return render_template("upload.html", user=username)


@app.route('/upload/<username>', methods=["POST", "GET"])
def get_file(username):

    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file != "":
            flash("File uploaded successfully!")
            name = uploaded_file.filename
            uploaded_file.save(os.path.join(UPLOAD_FOLDER, name))
            return redirect(url_for("stats", nm=name))


@app.route('/courses')
def courses():
    return render_template("new/courses.html", courses=course)




if __name__ == '__main__':
    app.run(debug=True)
