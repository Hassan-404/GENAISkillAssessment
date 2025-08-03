from typing import Optional, Dict, Any
from pydantic import BaseModel
from order_tracking import OrderSystem
from rag_system import PolicyRetriever


class ReturnProcessor:
    def __init__(self):
        self.order_system = OrderSystem()
        self.policy_retriever = PolicyRetriever()
        self._conversation_state = {}  # Stores multi-turn context

    def start_return(self, order_id: str) -> str:
        """Step 1: Verify order existence"""
        if not (order := self.order_system.get_order(order_id)):
            return "Order not found. Please verify your order ID."

        self._conversation_state = {
            'order_id': order_id,
            'eligible_items': [item['name'] for item in order['items']
                               if item.get('return_eligible', False)],
            'order_date': order['order_date']
        }

        eligible_count = len(self._conversation_state['eligible_items'])
        return (
            f"Order {order_id} found ({eligible_count} returnable items).\n"
            "Please provide:\n1. Return reason (defective/wrong_item/other)\n"
            "2. Comma-separated list of items"
        )

    def verify_policy(self, reason: str) -> str:
        """Step 2: Check reason against policy"""
        policy_response = self.policy_retriever.query(
            f"Return policy for {reason} within {self._conversation_state['order_date']}"
        )

        self._conversation_state.update({
            'reason': reason,
            'policy': policy_response
        })

        return (
            f" Policy Check:\n{policy_response}\n"
            f"Eligible items: {', '.join(self._conversation_state['eligible_items']) or 'None'}\n"
            " Please list items to return (comma-separated):"
        )

    def finalize_return(self, items_input: str) -> Dict[str, Any]:
        """Step 3: Validate items and generate return"""
        requested_items = [i.strip() for i in items_input.split(",")]
        valid_items = [
            item for item in requested_items
            if item in self._conversation_state['eligible_items']
        ]

        if not valid_items:
            return {
                'status': 'rejected',
                'reason': 'No eligible items specified',
                'eligible_items': self._conversation_state['eligible_items']
            }

        return {
            'status': 'approved',
            'return_id': f"RTN-{self._conversation_state['order_id']}-{hash(frozenset(valid_items))}",
            'items': valid_items,
            'policy_summary': self._conversation_state['policy'],
            'next_steps': (
                "1. Print return label (attached)\n"
                "2. Ship within 7 days\n"
                "3. Refund issued upon inspection"
            )
        }