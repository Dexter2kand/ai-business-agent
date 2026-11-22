
import sqlite3
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool

# Tool: Read customer information from SQLite
@tool
def get_customer_status(customer_id: str) -> str:
    """Look up a customer's request status using their ID."""
    with sqlite3.connect("customers.db") as conn:
        cursor = conn.execute(
            "SELECT name, status FROM customers WHERE id = ?",
            (customer_id,)
        )
        customer = cursor.fetchone()

    if customer is None:
        return f"No customer found with ID {customer_id}."

    return (
        f"Customer ID: {customer_id}, "
        f"Name: {customer[0]}, Status: {customer[1]}"
    )

# Connect to local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Create Agent
agent = create_agent(
    model=llm,
    tools=[get_customer_status],
    system_prompt=(
        "You are a business support assistant. "
        "Always use get_customer_status to check customer data. "
        "Never invent customer details."
    )
)


# Interactive AI Agent
print("Business AI Agent is ready!")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()

    if question.lower() == "exit":
        break

    if not question:
        continue

    try:
        result = agent.invoke({
            "messages": [
                {"role": "user", "content": question}
            ]
        })

        print("\nAI Agent:", result["messages"][-1].content)

        for message in result["messages"]:
            if getattr(message, "tool_calls", None):
                print("Tools used:", [
                    call["name"] for call in message.tool_calls
                ])

        print()

    except Exception as error:
        print("Error:", error)

