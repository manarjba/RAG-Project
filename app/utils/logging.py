# app/utils/logging.py
from pymongo import MongoClient
from datetime import datetime
from app.config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME


client = MongoClient("mongodb://mongo:27017")
db = client["rag_logs"]
collection = db["queries"]

def log_query(question, answer, sources):
    log = {
        "question": question,
        "answer": answer,
        "sources": sources,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(log)

def get_all_logs():
    logs = list(collection.find({}, {"_id": 0}))
    return logs
