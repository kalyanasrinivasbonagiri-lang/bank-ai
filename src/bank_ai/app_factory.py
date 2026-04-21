from __future__ import annotations

from pathlib import Path

from flask import Flask

from src.bank_ai.config import get_config
from src.bank_ai.rag.routes import register_blueprints
from src.bank_ai.utils.logging_utils import configure_logging


def create_app(config_object: type | None = None) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(Path(__file__).resolve().parents[2] / "templates"),
        static_folder=str(Path(__file__).resolve().parents[2] / "static"),
    )
    app.config.from_object(config_object or get_config())

    _ensure_directories(app)
    configure_logging(app)
    register_blueprints(app)

    @app.context_processor
    def inject_app_metadata() -> dict:
        return {
            "app_name": app.config["APP_NAME"],
            "sample_prompts": [
                "How to deposit money?",
                "How to withdraw money from ATM?",
                "What is KYC?",
                "How to fill a deposit slip?",
                "What documents are needed for withdrawal?",
            ],
        }

    return app


def _ensure_directories(app: Flask) -> None:
    for key in (
        "RAW_DATA_DIR",
        "PROCESSED_DATA_DIR",
        "UPLOAD_DIR",
        "VECTOR_DB_DIR",
        "LOG_DIR",
        "CACHE_DIR",
    ):
        Path(app.config[key]).mkdir(parents=True, exist_ok=True)
