from langchain_ollama import ChatOllama

# Connect Python to local AI model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)

# Send a message to AI
response = llm.invoke(
    "You are a business assistant. "
    "Explain what an AI Agent does in 2 sentences."
)

print("\nAI Response:")
print(response.content)
