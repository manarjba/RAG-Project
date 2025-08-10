# app/api/endpoints.py

from flask import Blueprint, request, jsonify
from app.utils.pdf_processor import extract_text_from_pdf, chunk_text
from app.utils.embeddings import generate_embedding
from app.database.chroma_client import add_embedding
from app.rag.chain import query_rag
from app.utils.logging import log_query, get_all_logs
from flasgger import swag_from
from app.models import QueryRequest, QueryResponse


api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/papers', methods=['POST'])
@swag_from({
    'tags': ['PDF Upload'],
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'files',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'Upload a single PDF file'
        }
    ],
    'responses': {
        200: {
            'description': 'File processed and stored successfully',
            'examples': {
                'application/json': {
                    'message': 'Files uploaded and processed',
                    'processed_files': ['example.pdf']
                }
            }
        },
        400: {
            'description': 'No file was uploaded'
        },
        500: {
            'description': 'Error processing file'
        }
    }
})
def upload_papers():
    if 'files' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['files']
    if file.filename == '':
        return jsonify({"error": "No file uploaded"}), 400

    text = extract_text_from_pdf(file)
    chunks = chunk_text(text)

    for i, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)
        if embedding:
            doc_id = f"{file.filename}_chunk_{i}"
            add_embedding(
                document_id=doc_id,
                embedding=embedding,
                metadata={"source": file.filename},
                text=chunk
            )

    return jsonify({
        "message": "Files uploaded and processed",
        "processed_files": [file.filename]
    })


@api_blueprint.route('/query', methods=['POST'])
@swag_from({
    'tags': ['Query'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': QueryRequest.schema()
        }
    ],
    'responses': {
        200: {
            'description': 'Answer generated from RAG',
            'schema': QueryResponse.schema()
        },
        400: {
            'description': 'Missing question in request body'
        },
        500: {
            'description': 'LLM generation failed'
        }
    }
})
def query_documents():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Missing 'question' in request body"}), 400

    question = data['question']

    try:
        answer, context_chunks, sources = query_rag(question)
    except Exception as e:
        return jsonify({"error": "LLM generation failed", "details": str(e)}), 500

    log_query(question, answer, sources)

    return jsonify({
        "question": question,
        "answer": answer,
        "sources": sources
    })


@api_blueprint.route('/logs/application', methods=['GET'])
@swag_from({
    'tags': ['Logs'],
    'responses': {
        200: {
            'description': 'List of logged questions, answers, and sources',
            'examples': {
                'application/json': {
                    "logs": [
                        {
                            "question": "What is Animal Farm about?",
                            "answer": "Animal Farm is a novel...",
                            "sources": ["sample.pdf"],
                            "timestamp": "Tue, 29 Jul 2025 17:07:29 GMT"
                        }
                    ]
                }
            }
        },
        500: {
            'description': 'Failed to retrieve logs'
        }
    }
})
def get_logs():
    try:
        logs = get_all_logs()
        return jsonify({"logs": logs})
    except Exception as e:
        return jsonify({"error": "Failed to retrieve logs", "details": str(e)}), 500
