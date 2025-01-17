from .models import db, SQLWatchlistPerson


class PostgreSQLDB:
    def __init__(self):
        self.session = db.session
        self.Model = db.Model
        self.WatchlistPerson = SQLWatchlistPerson

    def create_all(self):
        db.create_all()

    def add(self, obj):
        self.session.add(obj)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def query_all(self, model):
        return model.query.all()
