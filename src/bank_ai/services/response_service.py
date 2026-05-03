from __future__ import annotations

from src.bank_ai.constants.settings import LIMITATION_LINES


STEP_BY_STEP_CUES = (
    "step",
    "steps",
    "step by step",
    "process",
    "procedure",
    "guide me",
    "instructions",
    "how do i",
    "how can i",
)


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


def build_answer_style_instruction(query: str) -> str:
    lowered = query.lower()
    wants_steps = any(cue in lowered for cue in STEP_BY_STEP_CUES)

    if wants_steps:
        return (
            "Answer style: Give a customer-service explanation followed by short numbered steps. "
            "Start with 'This is the process to ...' when natural. Keep the list focused, usually 5 to 8 steps. "
            "Do not include every possible detail unless the user asks for full detail."
        )

    return (
        "Answer style: Respond like a helpful bank counter assistant. "
        "Do not jump straight into a long numbered list. Start with a short sentence explaining the process or requirement, "
        "then give the key points in a compact paragraph or a few bullets. "
        "Offer to provide step-by-step instructions if the user wants more detail."
    )


class ResponseService:
    def finalize_answer(self, answer: str, include_limitations: bool = False) -> str:
        cleaned = answer.strip()
        if not include_limitations:
            return cleaned

        limitations = "\n".join(f"- {line}" for line in LIMITATION_LINES)
        return f"{cleaned}\n\nLimitations:\n{limitations}"
