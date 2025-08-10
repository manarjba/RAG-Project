import chromadb
from chromadb.config import Settings
from app.config import CHROMA_PERSIST_PATH, CHROMA_COLLECTION_NAME

chroma_client = chromadb.PersistentClient(path=CHROMA_PERSIST_PATH)

collection = chroma_client.get_or_create_collection(name=CHROMA_COLLECTION_NAME)

def add_embedding(document_id, embedding, metadata, text):
    try:
        collection.upsert(
            ids=[document_id],
            embeddings=[embedding],
            metadatas=[metadata],
            documents=[text]
        )
        print(f"✅ Document {document_id} added to Chroma.")
    except Exception as e:
        print(f"❌ Error adding to Chroma: {str(e)}")

def query_similar(embedding, top_k=3):
    try:
        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        return results
    except Exception as e:
        print(f"❌ Error querying Chroma: {str(e)}")
        return None
