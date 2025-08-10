# app/main.py

from flask import Flask, jsonify, request
from app.utils.embeddings import generate_embedding
from app.utils.pdf_processor import extract_text_from_pdf
from app.database.chroma_client import add_embedding, query_similar, collection
from app.api.endpoints import api_blueprint
from app.rag.output_parser import parse_llm_output
from app.api.swagger import setup_swagger  # ✅ إعداد Swagger UI التفاعلي

app = Flask(__name__)

#  Swagger UI
setup_swagger(app)

app.register_blueprint(api_blueprint)

@app.route('/')
def home():
    return "🎉 Flask app is running inside Docker!"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
