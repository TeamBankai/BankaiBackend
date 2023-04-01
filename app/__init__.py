from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    cors = CORS(app)
    app.config["FLASK_DEBUG"] = True
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    from .models import Result

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
