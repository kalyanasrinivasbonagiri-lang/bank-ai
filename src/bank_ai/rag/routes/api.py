from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request

from src.bank_ai.schemas.chat import ChatResponse
from src.bank_ai.schemas.upload import UploadResponse
from src.bank_ai.services.chat_service import ChatService
from src.bank_ai.services.upload_service import UploadService
from src.bank_ai.utils.validators import validate_question


api_bp = Blueprint("api", __name__)


@api_bp.post("/chat")
def chat_api():
    payload = request.get_json(silent=True) or {}
    question = validate_question(payload.get("question", ""))
    answer = ChatService(current_app.config).answer(question)
    response = ChatResponse(answer=answer.answer, route=answer.route, sources=answer.sources)
    return jsonify(response.to_dict())


@api_bp.post("/upload")
def upload_api():
    upload = request.files.get("file")
    result = UploadService(current_app.config, ChatService(current_app.config).groq_client).save_and_extract(upload)
    response = UploadResponse(filename=result["filename"], extracted_text=result["text"])
    return jsonify(response.to_dict())
