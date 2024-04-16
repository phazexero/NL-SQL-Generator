import psycopg2
from sqlparse import format as sqlformat
from tables import get_table_names
from dotenv import load_dotenv
import os

load_dotenv()

host=os.environ["DB_HOST"],
port = os.environ["DB_PORT"],
database=os.environ["DB_NAME"],
user=os.environ["DB_USER"],
password=os.environ["DB_PASS"]

def get_create_table_statements(schema_name, host, port, database, user, password):
    statements = []
    try:
        conn = psycopg2.connect(
                    host=host,
                    port = port,
                    database=database,
                    user=user,
                    password=password
                )
        cursor = conn.cursor(host, port, database, user, password)

        # Get table names
        # cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s;", (schema_name,))
        table_names = get_table_names()

        for table_name in table_names:
        # Get column information and build CREATE TABLE statement
            statement = f"CREATE TABLE {schema_name}.{table_name} ("
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s;
            """, (schema_name, table_name))

        columns = cursor.fetchall()
        for i, (col_name, data_type, is_nullable) in enumerate(columns):
            null_def = " NOT NULL" if not is_nullable else ""
            statement += f"{col_name} {data_type}{null_def}"
            if i < len(columns) - 1:
                statement += ", "
            statement += ");"
        statements.append(statement)

        return statements

    except Exception as e:
        print(f"Error getting create table statements: {e}")
        return []

    finally:
        if conn:
            cursor.close()
        conn.close()

# Example usage (replace placeholders with your details)
statements = get_create_table_statements("public")
# print(statements)
if statements:
    # formatted_statements = [sqlformat(statement, reformat=True) for statement in statements]
    with open("schema_statements_formatted.sql", "w") as outfile:
        outfile.writelines(statements)
    print("Formatted CREATE TABLE statements written to schema_statements_formatted.sql")
else:
    print("No tables found in schema")