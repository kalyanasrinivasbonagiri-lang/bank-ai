from __future__ import annotations

from src.bank_ai.constants.settings import TOPIC_ALIASES
from src.bank_ai.rag.vector_store import build_vector_store


def retrieve_context(query: str, app_config) -> list[dict]:
    vector_store = build_vector_store(
        persist_directory=str(app_config["VECTOR_DB_DIR"]),
        collection_name=app_config["CHROMA_COLLECTION_NAME"],
        embedding_model_name=app_config["EMBEDDING_MODEL_NAME"],
    )
    expanded_query = expand_query(query)
    results = vector_store.similarity_search_with_score(expanded_query, k=app_config["TOP_K"])

    documents: list[dict] = []
    for document, score in results:
        documents.append(
            {
                "content": document.page_content,
                "metadata": document.metadata,
                "score": float(score),
            }
        )
    return documents


def expand_query(query: str) -> str:
    lowered = query.lower()
    expansions = [query]
    for canonical, synonyms in TOPIC_ALIASES.items():
        if canonical in lowered or any(word in lowered for word in synonyms):
            expansions.extend(synonyms)
    if any(term in lowered for term in ("how", "steps", "process", "procedure")):
        expansions.append("step by step process instructions")
    if any(term in lowered for term in ("fill", "form", "slip", "field", "details")):
        expansions.append("form fields explanation required details")
    if any(term in lowered for term in ("rule", "limit", "required", "mandatory", "guideline")):
        expansions.append("policy guideline rules requirements")
    return " ".join(dict.fromkeys(expansions))
