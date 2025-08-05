import os
from dotenv import load_dotenv
import pandas as pd
from vanna.google import GoogleGeminiChat # Correct for LLM
import chromadb # Correct for ChromaDB client
from vanna.chromadb import ChromaDB_VectorStore # Correct for Vanna's ChromaDB integration

import sqlite3
from backend.app.database import DATABASE_FILE, get_db_schema, get_db_connection

# Load environment variables
load_dotenv()

# --- Vanna Setup ---

# MyVanna should inherit from BOTH the LLM and the VectorStore
class MyVanna(ChromaDB_VectorStore, GoogleGeminiChat): 
    def __init__(self, config=None):
        # Initialize the ChromaDB client first
        chroma_db_path = os.path.join(os.path.dirname(__file__), '..', 'vanna_chroma_db')
        os.makedirs(chroma_db_path, exist_ok=True)
        chroma_client = chromadb.PersistentClient(path=chroma_db_path)

        # Initialize the ChromaDB_VectorStore base class
        ChromaDB_VectorStore.__init__(self, config={'client': chroma_client}) 

        # Initialize the GoogleGeminiChat base class
        GoogleGeminiChat.__init__(self, config=config)

        # Set the database path for SQL execution
        self.db_path = DATABASE_FILE

    # custom run_sql method
    def run_sql(self, sql: str) -> pd.DataFrame:
        """
        Executes the generated SQL query against the SQLite database.
        This method is called by Vanna.
        """
        conn = get_db_connection()
        if conn:
            try:
                df = pd.read_sql_query(sql, conn)
                return df
            except Exception as e:
                print(f"Error executing SQL: {e}")
                return pd.DataFrame({"error": [str(e)]})
            finally:
                conn.close()
        return pd.DataFrame({"error": ["Database connection failed."]})

    def get_ddl_for_table(self, table_name: str) -> str | None:
        """
        Overrides Vanna's default DDL retrieval for specific table.
        This helps Vanna get precise schema for the prompt.
        """
        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None

print("API Key Loaded:", os.getenv('GEMINI_API_KEY'))  # Debugging line to check if the API key is loaded correctly
# Initialize Vanna (pass the config to MyVanna, which then passes it to GoogleGeminiChat)
vn = MyVanna(config={'api_key': os.getenv('GEMINI_API_KEY'), 'model': 'gemini-2.5-flash'})

# --- Vanna Training (Run this once to train your agent) ---
def train_vanna():
    print("Starting Vanna training...")

    # 1. Train with DDL statements (Schema)
    ddl = get_db_schema()
    if ddl:
        vn.train(ddl=ddl)
        print("Trained with DDL statements.")
    else:
        print("Failed to get DDL statements for training.")

    # 2. Train with Documentation (explain business context or tricky columns)
    vn.train(documentation="The 'tracks' table contains information about individual songs, including their duration in milliseconds.")
    vn.train(documentation="The 'invoices' table contains sales data, and 'total' column represents the total amount for an invoice.")
    vn.train(documentation="Customer demographic information is in the 'customers' table.")
    print("Trained with documentation.")

    # 3. Train with Example SQL Queries (very important for accuracy)
    vn.train(question="Show me the total sales for each country",
             sql="SELECT BillingCountry, SUM(Total) FROM invoices GROUP BY BillingCountry ORDER BY SUM(Total) DESC;")

    vn.train(question="List the names of all artists",
             sql="SELECT Name FROM artists ORDER BY Name;")

    vn.train(question="How many tracks are in the Jazz genre?",
             sql="SELECT COUNT(T1.TrackId) FROM tracks AS T1 INNER JOIN genres AS T2 ON T1.GenreId = T2.GenreId WHERE T2.Name = 'Jazz';")

    vn.train(question="Who are the top 5 customers by total spending?",
             sql="SELECT C.FirstName, C.LastName, SUM(I.Total) AS TotalSpending FROM customers AS C JOIN invoices AS I ON C.CustomerId = I.CustomerId GROUP BY C.CustomerId ORDER BY TotalSpending DESC LIMIT 5;")

    print("Trained with example SQL queries.")
    print("Vanna training complete!")

# --- Function to Ask Vanna ---
def ask_vanna(question: str):
    """
    Asks Vanna a question, gets SQL, runs it, and returns the results.
    This version includes more robust error handling.
    """
    try:
        # Use generate_sql for explicitly getting the query string
        sql = vn.generate_sql(question=question)

        # -- ROBUSTNESS CHECK 1: Handle cases where the model returns no SQL --
        if sql is None:
            return {
                "sql": None,
                "results": None,
                "error": "The AI could not generate a SQL query for this question. Try rephrasing it."
            }

        # Run the generated SQL
        df = vn.run_sql(sql)
        
        # -- ROBUSTNESS CHECK 2: Handle cases where the SQL execution fails --
        # The run_sql method returns a DataFrame with an "error" column on failure
        if "error" in df.columns:
            return {"sql": sql, "results": None, "error": df["error"].iloc[0]}
        
        # If successful, convert the DataFrame to a dictionary
        results = df.to_dict(orient="records")
        return {"sql": sql, "results": results, "error": None}

    except Exception as e:
        # Catch any other unexpected errors during the process
        print(f"Error processing question: {e}") # Added print for debugging
        return {"sql": None, "results": None, "error": f"An unexpected error occurred: {str(e)}"}

if __name__ == '__main__':
    train_vanna()
    print("\n--- Testing Vanna Agent ---")

    question1 = "What are the names of the tables in the database?"
    response1 = ask_vanna(question1)
    print(f"\nQuestion: {question1}")
    print(f"SQL: {response1['sql']}")
    print(f"Results: {response1['results']}")
    print(f"Error: {response1['error']}")

    question2 = "Show the total sales per country."
    response2 = ask_vanna(question2)
    print(f"\nQuestion: {question2}")
    print(f"SQL: {response2['sql']}")
    print(f"Results: {response2['results']}")
    print(f"Error: {response2['error']}")

    question3 = "List the top 3 customers by spending."
    response3 = ask_vanna(question3)
    print(f"\nQuestion: {question3}")
    print(f"SQL: {response3['sql']}")
    print(f"Results: {response3['results']}")
    print(f"Error: {response3['error']}")