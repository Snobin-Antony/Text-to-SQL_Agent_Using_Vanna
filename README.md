# 🤖 Vanna Text-to-SQL Agent

Welcome to the Vanna Text-to-SQL Agent project\! This document outlines an intelligent AI agent designed to bridge the gap between human language and databases. It allows users to ask questions in plain English and receive precise, structured data in response, complete with the underlying SQL query that was generated.

This project leverages a powerful RAG (Retrieval-Augmented Generation) architecture to provide accurate, context-aware answers from a connected database.

## ✨ Features

  * **Natural Language to SQL:** Converts plain English questions into executable SQL queries.
  * **Interactive Chat Interface:** A pop-up chat modal provides a clean and intuitive user experience.
  * **Dynamic Dashboard:** Results are displayed clearly in a main dashboard area, separate from the chat input.
  * **Powered by Google Gemini:** Utilizes the `gemini-2.5-flash` model for fast and intelligent SQL generation.
  * **Persistent Knowledge Base:** Uses ChromaDB as a local vector database to store and retrieve knowledge about the database schema, ensuring the agent's responses are contextually relevant.
  * **Extensible Backend:** Built with FastAPI, providing a robust and scalable server environment.

## 🛠️ Tech Stack

### Backend

  * **Python 3.10+**
  * **FastAPI:** For building the high-performance web server.
  * **Vanna:** The core framework orchestrating the Text-to-SQL process.
  * **Google Gemini:** The Large Language Model used for reasoning.
  * **ChromaDB:** The vector database for storing and retrieving embeddings.
  * **Pandas:** For data manipulation and execution of SQL queries.

### Frontend

  * **React.js:** For building the user interface.
  * **JavaScript (ES6+)**
  * **CSS3:** For styling the components.

## 🏛️ Architecture

This project uses a **Retrieval-Augmented Generation (RAG)** architecture. This is a modern approach that avoids the need for expensive model fine-tuning.

The high-level flow is as follows:

`[React Frontend] <==> [FastAPI Server] <==> [Vanna Agent]`

The Vanna Agent itself is composed of three key parts:

1.  **The Brain (Gemini LLM):** Understands the user's question and the provided context to write SQL.
2.  **The Memory (ChromaDB):** Stores vector embeddings of the database schema, documentation, and example queries. When a new question is asked, Vanna retrieves the most relevant "memories" to help the brain.
3.  **The Data Source (SQLite):** The actual database where the final SQL query is executed.

## 🚀 Getting Started

Follow these instructions to get the project running locally on your machine.

### Prerequisites

  * Node.js and npm (for the frontend)
  * Python 3.10+ and pip (for the backend)

### Backend Setup

1.  **Clone the repository:**

    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Navigate to the backend directory and create a virtual environment:**

    ```bash
    cd backend
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    *(First, create a `requirements.txt` file if you haven't already)*

    ```bash
    pip freeze > requirements.txt
    ```

    *(Then install from the file)*

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create an environment file:**
    Create a file named `.env` in the root project directory and add your Google Gemini API key:

    ```
    GEMINI_API_KEY="your-actual-api-key"
    ```

5.  **Run the FastAPI server:**
    From the root project directory, run:

    ```bash
    uvicorn backend.app.main:app --reload
    ```

    The server will be running at `http://127.0.0.1:8000`.

### Frontend Setup

1.  **Navigate to the frontend directory:**
    *(Assuming your React app is in a `frontend` folder)*

    ```bash
    cd ../frontend 
    ```

2.  **Install dependencies:**

    ```bash
    npm install
    ```

3.  **Run the React development server:**

    ```bash
    npm start
    ```

    Your application will be available at `http://localhost:3000`.

## 📖 How to Use

1.  Ensure both the backend and frontend servers are running.
2.  Open your browser and navigate to `http://localhost:3000`.
3.  Click the "AI" button in the bottom-right corner to open the chat pop-up.
4.  Type a question about the data (e.g., "List all artists" for the sample data).
5.  Click "Ask". The generated SQL and the results table will appear on the main dashboard.

## 🔮 Future Improvements

  * **Custom Database Integration:** The agent is ready to be pointed at a custom database. This involves updating the connection logic and, most importantly, updating the training examples in `vanna_agent.py` to reflect the new data's business logic.
  * **Data Visualization:** Instead of just showing a table, the results could be rendered as charts or graphs for better data insights.
  * **Chat History:** Store the conversation history so users can see previous questions and answers.
  * **Evolve to an Agentic Model:** Transition from a pure RAG pattern to a tool-using agent. This would allow the agent to perform other actions, like sending an email with the results or searching the web for related information.