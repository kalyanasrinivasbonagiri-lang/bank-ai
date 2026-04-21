from __future__ import annotations

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.bank_ai.app_factory import create_app


def main() -> None:
    app = create_app()
    checks = {
        "raw_data_dir": Path(app.config["RAW_DATA_DIR"]).exists(),
        "upload_dir": Path(app.config["UPLOAD_DIR"]).exists(),
        "vector_db_dir": Path(app.config["VECTOR_DB_DIR"]).exists(),
        "groq_api_key_present": bool(app.config["GROQ_API_KEY"]),
    }

    for label, ok in checks.items():
        print(f"{label}: {'OK' if ok else 'MISSING'}")


if __name__ == "__main__":
    main()
