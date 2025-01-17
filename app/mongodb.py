from pymongo import MongoClient
from .models import WatchlistPerson
from flask import current_app


class MongoDB:
    def __init__(self):
        # Get MongoDB URI from config
        mongodb_uri = current_app.config["db_config"]["mongodb"]["uri"]
        self.client = MongoClient(mongodb_uri)
        self.db = self.client[current_app.config["db_config"]["mongodb"]["database"]]
        self.collection = self.db.watchlist_persons
        self.WatchlistPerson = WatchlistPerson

    def create_all(self):
        # MongoDB creates collections automatically
        pass

    def add(self, obj):
        # Convert model to dict and insert into MongoDB
        self.collection.insert_one(obj.to_dict())

    def commit(self):
        # MongoDB operations are atomic, no commit needed
        pass

    def rollback(self):
        # MongoDB operations are atomic, no rollback needed
        pass

    def query_all(self, model):
        # Get all documents and convert them to WatchlistPerson objects
        documents = self.collection.find()
        return [
            self.WatchlistPerson(
                image_path=doc["image_path"],
                source_url=doc["source_url"],
                reason=doc["reason"],
                year_taken=doc.get("year_taken"),
                id=str(doc["_id"]),
                created_at=doc.get("created_at"),
            )
            for doc in documents
        ]
