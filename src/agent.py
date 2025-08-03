from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from order_tracking import OrderSystem
from return_processing import ReturnProcessor
from config import Config
from prompt_templates import CustomerAgentPrompts

order_system = OrderSystem()
return_processor = ReturnProcessor()


@tool
def get_order_status(order_id=None, email=None):
    """Check order status using ID (formats: ORD1005/ORD-1005) or email."""
    if order := order_system.get_order(order_id, email):
        return (f"Order ID: {order['order_id']}\nStatus: {order['status'].upper()}\n"
                f"Tracking: {order.get('tracking_number', 'N/A')}\n"
                f"Items: {', '.join(i['name'] for i in order['items'])}")
    return "Order not found. Please check ID/email."


@tool
def handle_return_conversation(user_input: str, conversation_stage: str = None) -> str:
    """
    Multi-step return processor. Stages:
    - 'start': Initialize with order_id (e.g., "ORD-1005")
    - 'reason': Provide return reason (e.g., "defective")
    - 'items': List items to return (e.g., "headphones, case")
    """
    response = ""

    if not conversation_stage or conversation_stage == "start":
        response = return_processor.start_return(user_input)
    elif conversation_stage == "reason":
        response = return_processor.verify_policy(user_input)
    elif conversation_stage == "items":
        response = str(return_processor.finalize_return(user_input))

    return response or "Invalid conversation stage"


class CustomerAgent:
    def __init__(self):
        self.agent_executor = AgentExecutor(
            agent=create_openai_tools_agent(
                llm=ChatOpenAI(model=Config.LLM_MODEL, temperature=0),
                tools=[get_order_status, handle_return_conversation],
                prompt=CustomerAgentPrompts.get_system_prompt()),
            tools=[get_order_status, handle_return_conversation],
            verbose=True
        )

    def query(self, input_text: str) -> str:
        try:
            return self.agent_executor.invoke({"input": input_text})["output"]
        except Exception as e:
            return f"Error: {str(e)}"


if __name__ == "__main__":
    agent = CustomerAgent()

    # Test order lookup
    print(agent.query("Status for order ORD-1005?"))

    # Test return conversation
    print("\nRETURN PROCESS:")
    print(agent.query("I want to start a return for order ORD-1005"))  # start stage
    print(agent.query("defective"))  # reason stage
    print(agent.query("headphones, case"))  # items stage