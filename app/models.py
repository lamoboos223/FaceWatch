from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class WatchlistPerson(db.Model):
    __tablename__ = "watchlist_persons"

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    source_url = db.Column(db.String(500))
    year_taken = db.Column(db.Integer)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<WatchlistPerson {self.id}>"
