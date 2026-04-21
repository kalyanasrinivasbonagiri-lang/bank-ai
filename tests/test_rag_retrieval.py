from __future__ import annotations

from src.bank_ai.rag.retrieval import expand_query


def test_expand_query_for_deposit_keywords():
    query = "How to deposit money?"
    expanded = expand_query(query)
    assert "cash deposit" in expanded
    assert "step by step process instructions" in expanded
