from flask import Flask, current_app
from .models import db
from .postgresql import PostgreSQLDB
from .mongodb import MongoDB
from config import Config


def create_app():
    app = Flask(__name__)
    config = Config()
    app.config.from_object(config)

    # Get database configuration object
    db_config = config.get("database")

    # Store the database config in app.config for access elsewhere
    app.config["db_config"] = db_config

    if db_config["type"] == "postgresql":
        # PostgreSQL setup
        app.config["SQLALCHEMY_DATABASE_URI"] = db_config["postgresql"]["uri"]
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = db_config["postgresql"][
            "track_modifications"
        ]

        # Initialize PostgreSQL database
        db.init_app(app)
        with app.app_context():
            db.create_all()
    elif db_config["type"] == "mongodb":
        # MongoDB setup - no initialization needed
        pass
    else:
        raise ValueError(f"Unsupported database type: {db_config['type']}")

    from .routes import bp

    app.register_blueprint(bp)

    return app


def get_db():
    """Factory function to return the appropriate database instance"""

    # Get database configuration from app config
    db_config = current_app.config["db_config"]
    db_type = db_config["type"]

    if db_type == "postgresql":
        return PostgreSQLDB()
    elif db_type == "mongodb":
        return MongoDB()
    else:
        raise ValueError(f"Unsupported database type: {db_type}")
