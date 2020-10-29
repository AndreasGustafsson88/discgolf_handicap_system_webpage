from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from settings import db
# from flask_uploads import UploadSet, DATA
from flask_login import UserMixin

# csv_file = UploadSet("csv-file", DATA)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    score_card = db.Column(db.String(200), default="none")
    udisc_name = db.Column(db.String(100), default="none")
    udisc_rating = db.Column(db.Integer)
    metrix_rating = db.Column(db.Integer)
    pdga_rating = db.Column(db.Integer)


class UploadForm(FlaskForm):
    file = FileField(".csv", validators=[
        FileRequired(),
        FileAllowed(["csv"], message=".csv files only!")
    ])



