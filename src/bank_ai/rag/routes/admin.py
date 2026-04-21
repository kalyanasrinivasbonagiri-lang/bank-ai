from __future__ import annotations

from flask import Blueprint, current_app, jsonify

from src.bank_ai.llm.groq_client import GroqClient
from src.bank_ai.rag.indexing import index_documents


admin_bp = Blueprint("admin", __name__)


@admin_bp.post("/reindex")
def reindex():
    groq_client = GroqClient(
        api_key=current_app.config["GROQ_API_KEY"],
        text_model=current_app.config["GROQ_TEXT_MODEL"],
        vision_model=current_app.config["GROQ_VISION_MODEL"],
    )
    stats = index_documents(current_app.config, groq_client=groq_client)
    return jsonify({"status": "ok", "stats": stats})
