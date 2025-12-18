from rag.retriever import retrieve_context

def test_retriever_basic():
    context = retrieve_context("return policy")
    assert isinstance(context, list)
    assert len(context) >= 0

