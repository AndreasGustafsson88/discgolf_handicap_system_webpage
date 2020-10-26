from flask_sqlalchemy import SQLAlchemy

from settings.classes.database import Database

db = SQLAlchemy()

main_db = Database("Main")
main_db.update_database()

UPLOAD_FOLDER = "C:\\Kod\\Projekt\\handikapp_webpage\\uploads"
ALLOWED_FORMAT = (".csv",)
COURSE_DATA_PATH = "C:\\Kod\\Projekt\\Handicap system for Discgolf\\Course_data"

