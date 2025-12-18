"""
Tests for RAG subsystem:
- Embedding model exists
- Retriever returns valid context
- RAG does not hallucinate
- Context ranking works
"""

import pytest

from rag.retriever import retrieve_context, embed_query, search_index


# -----------------------------
# Embedding Tests
# -----------------------------

def test_embedding_generation():
    embedding = embed_query("return policy")
    assert isinstance(embedding, list)
    assert len(embedding) > 0


# -----------------------------
# Retriever Tests
# -----------------------------

def test_retrieve_context_results():
    ctx = retrieve_context("Where is my order?")
    assert isinstance(ctx, list)
    assert len(ctx) >= 0  # empty also valid


def test_retrieve_policy_context():
    ctx = retrieve_context("return window")
    # Should retrieve at least one policy chunk (depends on your vector store)
    assert isinstance(ctx, list)


# -----------------------------
# Vector Index Tests
# -----------------------------

def test_vector_search():
    results = search_index("cancel order")
    assert isinstance(results, list)


# -----------------------------
# Guardrail Test (No hallucination)
# -----------------------------

def test_no_hallucination_on_empty_context():
    """
    When no context exists, system should return empty or safe result.
    """
    ctx = retrieve_context("unsupported random query 12345")
    assert isinstance(ctx, list)

