def detect_intent(query: str):
    if "order" in query.lower():
        return "ORDER"
    if "price" in query.lower() or "quote" in query.lower():
        return "PRICING"
    if "return" in query.lower():
        return "RETURN"
    return "CATALOG"

