import fitz  # PyMuPDF
import io

def extract_text_from_pdf(file_storage):
    """
    Extracts text from a PDF file uploaded via Flask.
    """
    with fitz.open(stream=file_storage.read(), filetype="pdf") as pdf:
        text = ""
        for page in pdf:
            text += page.get_text()
    return text


def chunk_text(text, chunk_size=500, overlap=50):
    """
    Splits text into smaller chunks of a specified size with optional overlap.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunks.append(text[start:end])
        start += chunk_size - overlap

    return chunks
