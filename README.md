# AI Business Agent

A local, tool-enabled AI assistant for customer request tracking, PDF reporting, and simple business analytics. Built with **Python, Ollama, LangChain, Streamlit, and SQLite**.

## Features

- **Customer status lookup:** The agent uses a database-backed tool to retrieve a customer's name and request status by ID.
- **Local LLM:** Uses `qwen2.5:3b` through Ollama; model inference runs locally.
- **PDF reports:** A tool triggers generation of a PDF report of unfinished customer requests, with a download button in the Streamlit interface when the file exists.
- **Analytics dashboard:** Shows total customers, completed requests, open requests, and a status distribution chart using SQLite queries.
- **Standalone agent example:** `business_agent.py` demonstrates tool calling against a small in-memory sample dataset.

## Tech stack

Python · Streamlit · LangChain · langchain-ollama · Ollama · SQLite

## Project structure

```text
Business_Agent/
├── business_agent.py   # Standalone agent demo with sample customer data
├── dashboard.py        # Streamlit interface, agent tools, PDF download, analytics
├── database.py         # Database-related code
├── report_tool.py      # PDF report generation
├── agent.py            # Additional agent script
├── agent_backup.py     # Earlier agent version
├── sql_agent.py        # SQL-related agent script
└── .gitignore          # Excludes local databases, reports, and temporary files
```

## Getting started

**Prerequisites:** Python, Ollama, and a local SQLite customer database with the expected schema.

1. Install Python dependencies:

   ```bash
   pip install streamlit langchain langchain-ollama
   ```

   PDF generation may require additional packages; check `report_tool.py` for its imports.

2. Pull the model and start Ollama if it is not already running:

   ```bash
   ollama pull qwen2.5:3b
   ```

3. Set up `customers.db` locally. The dashboard expects a `customers` table with at least `id`, `name`, and `status` columns. The database is intentionally excluded from Git.

4. Launch the dashboard from the project directory:

   ```bash
   streamlit run dashboard.py
   ```

5. Ask a question such as: `What is the status of customer 1025?`

To run the standalone demonstration instead:

```bash
python business_agent.py
```

## Data and privacy

- Ollama performs model inference locally, but this alone does not establish end-to-end security.
- `customers.db`, generated PDFs, `.env`, and Python cache files should not be committed.
- Use **synthetic customer records** for public demonstrations; do not publish real customer data or credentials.
- This is a prototype, not a production-ready customer-management system.

## Planned improvements

- Sample database initialization and reproducible demo data
- Document ingestion and retrieval-augmented generation (RAG)
- Better error handling, tests, and dependency pinning
- User authentication and role-based access control

## License

No license has been selected yet.
