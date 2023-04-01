from flask import Flask
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///bankai"
    app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
    db.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
