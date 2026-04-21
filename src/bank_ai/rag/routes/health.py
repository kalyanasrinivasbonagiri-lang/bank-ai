from __future__ import annotations

from flask import Blueprint, current_app, jsonify

from src.bank_ai.schemas.health import HealthResponse


health_bp = Blueprint("health", __name__)


@health_bp.get("/")
def health_check():
    response = HealthResponse(status="ok", app_name=current_app.config["APP_NAME"])
    return jsonify(response.to_dict())
