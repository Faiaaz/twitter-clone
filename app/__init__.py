from flask import Flask
from flask_cors import CORS

from .extensions import db, bcrypt, login_manager
from .models import User, Tweet

from .routes.auth import auth_bp
from .routes.tweets import tweet_bp
from .routes.users import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    # Setup extensions
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"
    CORS(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tweet_bp)
    app.register_blueprint(user_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
