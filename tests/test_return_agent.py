from agents.return_agent import handle_return_request

def test_return_eligible():
    resp = handle_return_request("ORD1001", "SKU1001")
    assert resp["eligible"] in [True, False]
    assert "refund_amount" in resp
    assert "message" in resp

