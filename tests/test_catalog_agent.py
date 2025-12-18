import pytest
from agents.catalog_agent import handle_catalog_query

def test_catalog_agent_basic():
    query = "show phones"
    result = handle_catalog_query(query)

    assert "products" in result
    assert isinstance(result["products"], list)
    assert result["message"]

