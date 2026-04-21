from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter


def build_text_splitter() -> RecursiveCharacterTextSplitter:
    return RecursiveCharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=120,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
