
import streamlit as st
from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
import sqlite3
from report_tool import generate_customer_report

@tool
def create_pdf_report() -> str:
    """Generate a PDF report of all unfinished customer requests."""
    filename = generate_customer_report()
    return f"PDF report created successfully: {filename}"
@tool
def get_customer_status(customer_id: str) -> str:
    """Get customer status from the database using customer ID."""
    with sqlite3.connect("customers.db") as conn:
        customer = conn.execute(
            "SELECT name, status FROM customers WHERE id = ?",
            (customer_id,)
        ).fetchone()

    if customer is None:
        return "Customer not found."

    return f"Customer: {customer[0]}, Status: {customer[1]}"

@st.cache_resource
def load_agent():
    llm = ChatOllama(model="qwen2.5:3b", temperature=0)
    return create_agent(
        model=llm,
        tools=[get_customer_status, create_pdf_report],
        system_prompt=(
            "You are a business support assistant. "
            "Always use the tool to verify customer information. "
            "Never invent customer details."
        )
    )

st.title("🤖 Business AI Agent")
st.caption("Python + Ollama + LangChain + SQLite")

agent = load_agent()

question = st.text_input(
    "Ask about a customer:",
    placeholder="What is the status of customer 1025?"
)

if st.button("Ask Agent"):
    if question.strip():
        with st.spinner("AI Agent is analyzing..."):
            try:
                result = agent.invoke({
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                })
                st.success(result["messages"][-1].content)
            except Exception as error:
                st.error(str(error))


from pathlib import Path

# PDF Download Button
pdf_path = Path(__file__).resolve().parent / "customer_report.pdf"

if pdf_path.exists():
    st.divider()
    st.subheader("📄 Customer Report")

    st.download_button(
        label="⬇️ Download PDF Report",
        data=pdf_path.read_bytes(),
        file_name="customer_report.pdf",
        mime="application/pdf",
        use_container_width=True
    )


# AI Analytics Dashboard
st.divider()
st.header("📊 Business Analytics")

with sqlite3.connect("customers.db") as conn:
    rows = conn.execute(
        "SELECT status, COUNT(*) FROM customers GROUP BY status"
    ).fetchall()

stats = dict(rows)

total = sum(stats.values())
completed = stats.get("Completed", 0)
open_requests = total - completed

col1, col2, col3 = st.columns(3)

col1.metric("Total Customers", total)
col2.metric("Completed", completed)
col3.metric("Open Requests", open_requests)

st.subheader("Customer Status Distribution")

st.bar_chart(
    {
        "Pending": stats.get("Pending", 0),
        "Processing": stats.get("Processing", 0),
        "Completed": completed
    },
    x_label="Customer Status",
    y_label="Number of Customers"
)

st.caption("Live analytics from SQLite database")

