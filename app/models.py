from datetime import datetime


class WatchlistPerson:
    """Generic WatchlistPerson model"""

    def __init__(
        self, image_path, source_url, reason, year_taken=None, id=None, created_at=None
    ):
        self.id = id
        self.image_path = image_path
        self.source_url = source_url
        self.year_taken = year_taken
        self.reason = reason
        self.created_at = created_at or datetime.utcnow()

    def to_dict(self):
        return {
            "id": self.id,
            "image_path": self.image_path,
            "source_url": self.source_url,
            "year_taken": self.year_taken,
            "reason": self.reason,
            "created_at": self.created_at,
        }

    def __repr__(self):
        return f"<WatchlistPerson {self.id}>"


# SQLAlchemy specific implementation
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class SQLWatchlistPerson(db.Model, WatchlistPerson):
    __tablename__ = "watchlist_persons"

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    source_url = db.Column(db.String(500))
    year_taken = db.Column(db.Integer)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
