from pymongo import MongoClient

_client = None
_db = None

def get_db():
    global _client, _db
    if _client is None:
        _client = MongoClient("mongodb://localhost:27017")
        _db = _client["hospital_db"]
    return _db
