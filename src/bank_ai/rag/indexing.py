from __future__ import annotations

from pathlib import Path

import fitz
from langchain_core.documents import Document

from src.bank_ai.ocr.extraction import extract_text_from_file
from src.bank_ai.rag.chunking import build_text_splitter
from src.bank_ai.rag.loaders import iter_source_documents, load_text_document
from src.bank_ai.rag.vector_store import build_vector_store


def index_documents(app_config, groq_client=None) -> dict[str, int]:
    vector_store = build_vector_store(
        persist_directory=str(app_config["VECTOR_DB_DIR"]),
        collection_name=app_config["CHROMA_COLLECTION_NAME"],
        embedding_model_name=app_config["EMBEDDING_MODEL_NAME"],
    )
    source_files = iter_source_documents(app_config["RAW_DATA_DIR"])
    splitter = build_text_splitter()
    documents: list[Document] = []

    for path in source_files:
        text = _extract_source_text(path, groq_client)
        if not text.strip():
            continue

        for chunk_index, chunk in enumerate(splitter.split_text(text)):
            documents.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": str(path),
                        "filename": path.name,
                        "topic": path.parent.name,
                        "chunk_index": chunk_index,
                    },
                )
            )

    if documents:
        vector_store.delete_collection()
        vector_store = build_vector_store(
            persist_directory=str(app_config["VECTOR_DB_DIR"]),
            collection_name=app_config["CHROMA_COLLECTION_NAME"],
            embedding_model_name=app_config["EMBEDDING_MODEL_NAME"],
        )
        vector_store.add_documents(documents)

    return {"files_indexed": len(source_files), "chunks_indexed": len(documents)}


def _extract_source_text(path: Path, groq_client=None) -> str:
    if path.suffix.lower() == ".txt":
        return load_text_document(path)
    if path.suffix.lower() == ".pdf":
        try:
            document = fitz.open(path)
            try:
                collected = [document.load_page(i).get_text("text") for i in range(document.page_count)]
                text = "\n".join(collected).strip()
                if text:
                    return text
            finally:
                document.close()
        except Exception:
            pass

        if groq_client:
            return extract_text_from_file(path, groq_client)
    return ""
