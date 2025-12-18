def calculate_price(customer_tier, base_price, quantity):
    discount = 0
    if customer_tier == "GOLD":
        discount = 0.15
    elif customer_tier == "SILVER":
        discount = 0.10

    final_price = base_price * quantity * (1 - discount)
    return {
        "tier": customer_tier,
        "discount": discount,
        "final_price": final_price
    }

