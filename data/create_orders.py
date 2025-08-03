# save as create_orders.py in your project root
import json
from pathlib import Path

data = [
    {
        "order_id": "ORD-1001",
        "customer_email": "user1@example.com",
        "status": "shipped",
        "tracking_number": "UPS-12345",
        "items": [
            {"product_id": "P-101", "name": "Wireless Headphones", "return_eligible": True}
        ],
        "order_date": "2024-05-15"
    }
]

# Create data directory if not exists
Path("data").mkdir(exist_ok=True)

# Write fresh file
with open("orders.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("orders.json created successfully at:", Path("orders.json").absolute())