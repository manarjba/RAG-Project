# app/utils/embeddings.py

import requests

def generate_embedding(text):
    url = "http://ollama:11434/api/embeddings"
    payload = {
        "model": "nomic-embed-text",
        "prompt": text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        if "embedding" in data:
            return data["embedding"]
        else:
            print(f"Embedding not found in response: {data}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error generating embedding: {e}")
        return None
