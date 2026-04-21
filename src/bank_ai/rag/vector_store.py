from __future__ import annotations

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


def build_embeddings(model_name: str):
    return HuggingFaceEmbeddings(model_name=model_name)


def build_vector_store(persist_directory: str, collection_name: str, embedding_model_name: str) -> Chroma:
    embeddings = build_embeddings(embedding_model_name)
    return Chroma(
        collection_name=collection_name,
        persist_directory=persist_directory,
        embedding_function=embeddings,
    )
