# app/config.py

CHROMA_PERSIST_PATH = "/app/chroma"
CHROMA_COLLECTION_NAME = "documents"

#  MongoDB
MONGO_URI = "mongodb://mongo:27017/"
MONGO_DB_NAME = "rag_logs"
MONGO_COLLECTION_NAME = "application_logs"

#  Ollama
OLLAMA_API_URL = "http://ollama:11434/api/generate"
OLLAMA_MODEL = "llama2"