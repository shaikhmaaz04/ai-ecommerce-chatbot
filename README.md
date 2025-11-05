# 🛒 AI E-Commerce Chatbot

This is an intelligent, multi-faceted AI chatbot designed for e-commerce platforms. It uses a semantic router to understand user intent and delegate tasks to specialized agents.

This bot can:

  * Answer **general questions** (FAQs) about policies using a RAG pipeline.
  * Answer **product-specific questions** by converting natural language into SQL queries.
  * Handle **casual conversation** (small talk) to be more engaging.

-----

### 🚀 Features

  - **Intelligent Query Routing:** Uses `semantic-router` to accurately classify user intent and route the query to the correct handler (`faq`, `sql`, or `small-talk`).
  - **RAG-based FAQ:** Answers common questions (e.g., "What is your return policy?") by retrieving relevant information from a **ChromaDB** vector store.
  - **Natural Language to SQL:** Translates product-specific requests (e.g., "Show me Puma shoes under 5000") into SQL queries, runs them against a **SQLite** database, and formats the results.
  - **Conversational AI:** Handles casual chit-chat (e.g., "How are you?") using a separate, friendly prompt via **Groq**.
  - **Interactive UI:** Built with **Streamlit** for a clean, real-time chat interface.

-----

### 🧰 Tech Stack

| Component | Technology |
| --- | --- |
| Framework | Streamlit |
| LLM Provider | Groq |
| Routing | semantic-router |
| Vector DB | ChromaDB |
| Product DB | SQLite |
| Embeddings | HuggingFace (`gte-base`, `all-MiniLM-L6-v2`) |
| Data Handling | Pandas |

-----

### 🧩 How It Works

1.  A user enters a query in the Streamlit UI.
2.  The query is first sent to the **`semantic-router`** (`router.py`).
3.  The router classifies the query's intent based on its semantic meaning.
4.  The query is then passed to the chosen agent:
      * **`faq`**: The query is sent to the `faq_chain` (`faq.py`). It performs a similarity search in ChromaDB to find the most relevant Q\&A, passes this context to Groq, and returns a RAG-based answer.
      * **`sql`**: The query is sent to the `sql_chain` (`sql.py`). Groq generates a SQL query based on the user's request and the database schema. This query is run against the SQLite database, and the resulting data is passed *back* to Groq to be formatted into a user-friendly, natural language response.
      * **`small-talk`**: The query is sent directly to the `small_talk` function (`small_talk.py`), which uses a specific system prompt for friendly, casual conversation with Groq.
5.  The final response from the agent is displayed in the Streamlit chat window.

-----

## ⚙️ Setup

### 1\. Prerequisites

This project requires a `db.sqlite` file (for products) and a `resources/faq_data.csv` file (for FAQs).

  * The **product database** schema is defined in `app/sql.py`.
  * The **FAQ data** should be a CSV with `question` and `answer` columns.

### 2\. Environment Variables

Create a `.env` file in the project's root directory (alongside the `app` folder). Add your Groq API key and the model you wish to use:

```bash
GROQ_API_KEY="your_groq_api_key_here"
GROQ_MODEL="llama3-70b-8192"
```

### 3\. Install Dependencies

You can use either `pip` or `uv`.

#### 🧩 Option A — Using `pip`

Install all dependencies from your `requirements.txt` file:

```bash
pip install -r requirements.txt
```

-----

#### ⚡ Option B — Using `uv` (Recommended)

[`uv`](https://www.google.com/search?q=%5Bhttps://github.com/astral-sh/uv%5D\(https://github.com/astral-sh/uv\)) is an extremely fast Python package installer and resolver.

1.  **Install `uv`** (if you don't have it)
    ```bash
    # macOS / Linux
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Windows
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```
2.  **Sync dependencies**
    `uv` will read your `pyproject.toml` or `requirements.txt` file and install the dependencies into a new virtual environment.
    ```bash
    uv sync
    ```
    *(This will automatically create a virtual environment (`.venv`) and install all dependencies.)*

-----

### 🏃‍♂️ Run the App

1.  Open your terminal.
2.  If you used `uv` (or a manual venv), activate the virtual environment:
    ```bash
    source .venv/bin/activate
    # On Windows: .venv\Scripts\activate
    ```
3.  Run the Streamlit app:
    ```bash
    streamlit run app/main.py
    ```

The first time you run the app, the `ingest_faq_data` function will be called automatically to populate the ChromaDB vector store. On subsequent runs, it will detect the existing collection and skip ingestion.