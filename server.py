from flask import Flask
from settings import *
from flask_login import LoginManager

app = Flask(__name__)




app.config["SECRET_KEY"] = "supersecret, don't tell"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///db2.sqlite'
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)


if __name__ == "__main__":
    app.run(debug=True)

    # db.create_all(app=app)
