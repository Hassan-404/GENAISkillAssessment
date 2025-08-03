import json
from config import Config

class OrderSystem:
    def __init__(self):
        self.orders = self._load_orders()

    def _load_orders(self):
        with open(Config.MOCK_ORDERS) as f:
            return json.load(f)

    def get_order(self, order_id=None, email=None):
        if order_id:
            # Normalize order ID by removing spaces/hyphens
            normalized_id = order_id.replace(" ", "").replace("-", "")
            for order in self.orders:
                if normalized_id == order['order_id'].replace(" ", "").replace("-", ""):
                    return order
        if email:
            for order in self.orders:
                if email.lower() == order['customer_email'].lower():
                    return order
        return None
