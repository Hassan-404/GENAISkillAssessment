from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

class CustomerAgentPrompts:
    @staticmethod
    def get_system_prompt():
        return ChatPromptTemplate.from_messages([
            ("system", """You are a helpful e-commerce customer service assistant. 
             Follow these rules strictly:
             1. Be polite and professional
             2. When checking order status, always verify either:
                - Order ID
                - Customer email
             3. For returns, clearly explain eligibility based on policies
             4. For policy questions, use the policy knowledge base tool"""),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad")
        ])