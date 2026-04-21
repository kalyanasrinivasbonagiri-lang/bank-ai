from __future__ import annotations

from pathlib import Path

from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from src.bank_ai.ocr.extraction import extract_text_from_file
from src.bank_ai.utils.validators import validate_upload_extension


class UploadService:
    def __init__(self, app_config, groq_client):
        self.app_config = app_config
        self.groq_client = groq_client

    def save_and_extract(self, upload: FileStorage) -> dict:
        if not upload or not upload.filename:
            raise ValueError("No file was uploaded.")

        validate_upload_extension(upload.filename, self.app_config["SUPPORTED_UPLOAD_EXTENSIONS"])
        filename = secure_filename(upload.filename)
        destination = Path(self.app_config["UPLOAD_DIR"]) / filename
        upload.save(destination)
        text = extract_text_from_file(destination, self.groq_client)

        return {
            "filename": filename,
            "path": str(destination),
            "text": text,
        }
