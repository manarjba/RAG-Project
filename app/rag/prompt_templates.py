# app/rag/prompt_templates.py

def build_prompt(context_chunks: list[str], question: str) -> str:
    """
    Constructs a full prompt to send to the LLM using retrieved context and the user question.
    """
    system_prompt = (
        "You are an academic assistant tasked with answering questions based on provided research excerpts. "
        "Use only the information from the context below. If the answer is not in the context, say 'I don't know'. "
        "Cite the source of each part of the answer by the document name if available."
    )

    context = "\n\n".join(f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks))

    full_prompt = (
        f"{system_prompt}\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        f"Answer:"
    )

    return full_prompt
