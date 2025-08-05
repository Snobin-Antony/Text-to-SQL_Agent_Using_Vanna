import sqlite3
import os

DATABASE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'chinook.db')

def get_db_connection():
    conn = None
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        conn.row_factory = sqlite3.Row # This makes results accessible by column name
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

def get_db_schema():
    """Fetches the DDL (schema) of the Chinook database."""
    conn = get_db_connection()
    if not conn:
        return ""

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    ddl_statements = []
    for table in tables:
        table_name = table[0]
        cursor.execute(f"PRAGMA table_info('{table_name}');")
        columns = cursor.fetchall()
        
        create_table_sql = f"CREATE TABLE {table_name} (\n"
        column_definitions = []
        for col in columns:
            cid, name, ctype, notnull, dflt_value, pk = col
            col_def = f"  {name} {ctype}"
            if notnull:
                col_def += " NOT NULL"
            if pk:
                col_def += " PRIMARY KEY"
            column_definitions.append(col_def)
        create_table_sql += ",\n".join(column_definitions)
        
        # Add foreign keys if possible (more complex for general SQLite, but can be done manually or parsed if needed)
        # For Chinook, we'd typically add these manually or find a script.
        # For simplicity, we'll just get table and column definitions here.

        create_table_sql += "\n);\n"
        ddl_statements.append(create_table_sql)

    conn.close()
    return "\n".join(ddl_statements)

if __name__ == "__main__":
    # Test connection and schema retrieval
    conn = get_db_connection()
    if conn:
        print("Successfully connected to chinook.db")
        conn.close()
    else:
        print("Failed to connect to chinook.db")

    schema = get_db_schema()
    if schema:
        print("\n--- Chinook Database Schema (DDL) ---")
        print(schema)
    else:
        print("\nFailed to retrieve schema.")