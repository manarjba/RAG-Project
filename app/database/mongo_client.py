# app/database/mongo_client.py

from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = "rag_logs"
COLLECTION_NAME = "queries"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]


def log_query(question: str, context: list[str], answer: str, source_docs: list[str] = None):
    """
    Logs the user's query, answer, and context to the MongoDB database.
    """
    entry = {
        "timestamp": datetime.utcnow(),
        "question": question,
        "context_chunks": context,
        "answer": answer,
        "sources": source_docs or [],
    }
    collection.insert_one(entry)
