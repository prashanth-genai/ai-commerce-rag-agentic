import requests

def handle_order(user_id):
    response = requests.get(
        f"http://java-commerce-mock/order-service/orders/{user_id}"
    )
    return response.json()

