from flask import Flask
from .extensions import db, bcrypt, login_manager
from .models import User, Tweet
from flask_cors import CORS


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    CORS(app)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    with app.app_context():
        db.create_all()

    return app
