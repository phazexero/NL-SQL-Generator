import psycopg2
from table_names import get_table_names 
from dotenv import load_dotenv
import os

load_dotenv()

host=os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
database=os.environ["DB_NAME"]
user=os.environ["DB_USER"]
password=os.environ["DB_PASS"]

def get_create_table_statements(host, port, database, user, password, schema_name):
    statements = []
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
        )
        cursor = conn.cursor()

        # Get table names
        table_names = get_table_names(host, port, database, user, password)

        for table_name in table_names:
            # Get column information and build CREATE TABLE statement
            statement = f"CREATE TABLE {schema_name}.{table_name} (\n"  # Add newline for better formatting

            cursor.execute(
                """
                SELECT column_name, data_type, is_nullable, CHARACTER_MAXIMUM_LENGTH
                FROM information_schema.columns
                WHERE table_schema = %s AND table_name = %s;
                """,
                (schema_name, table_name),
            )

            columns = cursor.fetchall()
            for i, (col_name, data_type, is_nullable, max_length) in enumerate(columns):
                null_def = " NOT NULL" if not is_nullable else ""

                # Add character length if data_type is varchar and max_length is available
                if data_type.lower() == "character varying" and max_length is not None:
                    data_type += f"({max_length})"

                # Indent each column definition
                statement += f"\t{col_name} {data_type}{null_def}"
                if i < len(columns) - 1:
                    statement += ",\n"  # Add comma and newline for each column except the last

            statement += "\n);\n"  # Add newline before and after closing parenthesis
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
statements = get_create_table_statements(host, port, database, user, password, "public")
# print(statements)
if statements:
    # formatted_statements = [sqlformat(statement, reformat=True) for statement in statements]
    with open("../metadata.sql", "w") as outfile:
        outfile.writelines(statements)
    print("Formatted CREATE TABLE statements written to schema_statements_formatted.sql")
else:
    print("No tables found in schema")