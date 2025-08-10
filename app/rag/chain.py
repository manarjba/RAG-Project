# app/rag/chain.py

import requests
import json
from app.config import OLLAMA_API_URL, OLLAMA_MODEL
from app.utils.embeddings import generate_embedding
from app.database.chroma_client import query_similar
from app.rag.prompt_templates import build_prompt
from app.rag.output_parser import parse_response


def query_rag(question: str):
    """
    Executes the RAG chain and returns the answer, context chunks, and sources.
    """
    # 1. Generate embedding
    embedding = generate_embedding(question)
    if embedding is None:
        return "❌ Failed to generate embedding.", [], []

    # 2. Retrieve context from Chroma
    results = query_similar(embedding, top_k=3)
    if not results or "documents" not in results:
        return "❌ Failed to retrieve documents.", [], []

    context_chunks = results["documents"]
    metadatas = results.get("metadatas", [[]])[0]
    source_docs = [meta.get("source", "unknown") for meta in metadatas]

    # 3. Build prompt
    prompt = build_prompt(context_chunks, question)

    # 4. Send to Ollama (stream response)
    try:
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt},
            stream=True
        )
        if response.ok:
            full_text = ""
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line.decode('utf-8'))
                        full_text += chunk.get("response", "")
                    except json.JSONDecodeError:
                        continue
            answer = parse_response(full_text)
            return answer, context_chunks, source_docs
        else:
            return f"❌ Ollama error: {response.status_code}", context_chunks, source_docs
    except Exception as e:
        return f"❌ Exception: {str(e)}", context_chunks, source_docs
