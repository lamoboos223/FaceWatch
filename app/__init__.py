from flask import Flask
from .models import db


def create_app():
    app = Flask(__name__)

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "postgresql://facewatch:facewatch@localhost/facewatch"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    from .routes import bp

    app.register_blueprint(bp)

    return app
