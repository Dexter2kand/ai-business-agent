from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool

# Sample customer database
customers = {
    "1025": {
        "name": "John Smith",
        "status": "Processing"
    },
    "1026": {
        "name": "Anna Müller",
        "status": "Completed"
    },
    "1027": {
        "name": "David Brown",
        "status": "Pending"
    }
}

# Tool available to the AI Agent
@tool
def get_customer_status(customer_id: str) -> str:
    """Get a customer's request status by customer ID."""
    customer = customers.get(customer_id)

    if customer is None:
        return "Customer not found."

    return (
        f"Customer: {customer['name']}, "
        f"Status: {customer['status']}"
    )

# Local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Create AI Agent
agent = create_agent(
    model=llm,
    tools=[get_customer_status],
    system_prompt=(
        "You are a customer support AI agent. "
        "Always use the available tool to check customer status. "
        "Never invent customer information."
    )
)

# Ask the Agent
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "What is the status of customer 1025?"
        }
    ]
})

print("\nAI Agent Response:")
print(result["messages"][-1].content)
