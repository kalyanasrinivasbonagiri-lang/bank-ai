from __future__ import annotations

from pathlib import Path
import sys


ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from src.bank_ai.app_factory import create_app
from src.bank_ai.llm.groq_client import GroqClient
from src.bank_ai.rag.indexing import index_documents


def main() -> None:
    app = create_app()
    with app.app_context():
        groq_client = GroqClient(
            api_key=app.config["GROQ_API_KEY"],
            text_model=app.config["GROQ_TEXT_MODEL"],
            vision_model=app.config["GROQ_VISION_MODEL"],
        )
        stats = index_documents(app.config, groq_client=groq_client)
        print(f"Indexed {stats['files_indexed']} files into {stats['chunks_indexed']} chunks.")


if __name__ == "__main__":
    main()
