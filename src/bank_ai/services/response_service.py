from __future__ import annotations

from src.bank_ai.constants.settings import LIMITATION_LINES


def format_context_block(documents: list[dict]) -> str:
    blocks = []
    for index, item in enumerate(documents, start=1):
        metadata = item.get("metadata", {})
        blocks.append(
            f"[Source {index}] topic={metadata.get('topic', 'unknown')} file={metadata.get('filename', 'unknown')}\n"
            f"{item.get('content', '').strip()}"
        )
    return "\n\n".join(blocks)


def build_source_list(documents: list[dict]) -> list[dict]:
    seen = set()
    sources = []
    for item in documents:
        metadata = item.get("metadata", {})
        source_key = metadata.get("source")
        if source_key in seen:
            continue
        seen.add(source_key)
        sources.append(
            {
                "source": metadata.get("source", ""),
                "filename": metadata.get("filename", ""),
                "topic": metadata.get("topic", ""),
            }
        )
    return sources


class ResponseService:
    def finalize_answer(self, answer: str, include_limitations: bool = False) -> str:
        cleaned = answer.strip()
        if not include_limitations:
            return cleaned

        limitations = "\n".join(f"- {line}" for line in LIMITATION_LINES)
        return f"{cleaned}\n\nLimitations:\n{limitations}"
