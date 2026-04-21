from __future__ import annotations

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


class Config:
    APP_NAME = "BankAI"
    DEBUG = False
    TESTING = False

    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", "5000"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "bank-ai-secret")
    SESSION_COOKIE_NAME = "bank_ai_session"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)

    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    GROQ_TEXT_MODEL = "llama-3.3-70b-versatile"
    GROQ_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

    DATA_DIR = BASE_DIR / "data"
    RAW_DATA_DIR = DATA_DIR / "raw"
    PROCESSED_DATA_DIR = DATA_DIR / "processed"
    UPLOAD_DIR = DATA_DIR / "uploads"

    STORAGE_DIR = BASE_DIR / "storage"
    VECTOR_DB_DIR = STORAGE_DIR / "vector_db"
    LOG_DIR = STORAGE_DIR / "logs"
    CACHE_DIR = STORAGE_DIR / "cache"

    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
    CHROMA_COLLECTION_NAME = "bank_ai_guidance"
    TOP_K = 4
    MAX_CHAT_HISTORY = 8
    MAX_UPLOAD_SIZE_MB = 10
    SUPPORTED_UPLOAD_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".txt"}


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    VECTOR_DB_DIR = BASE_DIR / "storage" / "test_vector_db"
    CHROMA_COLLECTION_NAME = "bank_ai_test"


def get_config() -> type[Config]:
    env = os.getenv("FLASK_ENV", "development").lower()
    if env == "testing":
        return TestingConfig
    if env == "production":
        return Config
    return DevelopmentConfig
