from __future__ import annotations

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from src.bank_ai.constants.settings import BANKING_DISCLAIMER, LIMITATION_LINES
from src.bank_ai.extensions import session_service
from src.bank_ai.services.chat_service import ChatService
from src.bank_ai.services.upload_service import UploadService
from src.bank_ai.utils.validators import validate_question


web_bp = Blueprint("web", __name__)


@web_bp.get("/")
def index():
    return render_template(
        "index.html",
        messages=session_service.get_messages(),
        disclaimer=BANKING_DISCLAIMER,
        limitation_lines=LIMITATION_LINES,
    )


@web_bp.post("/chat")
def chat():
    try:
        question = validate_question(request.form.get("question", ""))
        answer = ChatService(current_app.config).answer(question)
        flash("Answer generated successfully.", "success")
        return render_template(
            "index.html",
            messages=session_service.get_messages(),
            answer=answer,
            disclaimer=BANKING_DISCLAIMER,
            limitation_lines=LIMITATION_LINES,
        )
    except ValueError as exc:
        flash(str(exc), "error")
        return redirect(url_for("web.index"))


@web_bp.post("/upload")
def upload():
    upload = request.files.get("file")
    try:
        result = UploadService(current_app.config, ChatService(current_app.config).groq_client).save_and_extract(upload)
        session_service.set_uploaded_context(result["text"])
        session_service.add_message("assistant", f"Uploaded file processed: {result['filename']}")
        flash(f"Uploaded and processed: {result['filename']}", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("web.index"))


@web_bp.post("/reset")
def reset_chat():
    session_service.clear()
    flash("Chat session cleared.", "success")
    return redirect(url_for("web.index"))
