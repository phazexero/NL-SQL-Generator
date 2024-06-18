import psycopg2
from table_names import get_table_names 
from databases import Database
from repositories.data_fetch_repository import get_metadata
from repositories.data_fetch_repository import get_names

async def get_table_names(db: Database):
    return await get_names(db)

async def get_table_structure(db: Database, sname: str, tname: str):
    return await get_metadata(db, sname, tname)

def get_create_table_statements(schema_name):
    statements = []

    all_names = [row[0] for row in get_table_names()]
    table_names = []
    if table_names:
        print("Tables in schema", schema_name, ":")
        for table in all_names:
            table_names.append(table)

    for table_name in table_names:
        # Get column information and build CREATE TABLE statement
        statement = f"CREATE TABLE {schema_name}.{table_name} (\n"  # Add newline for better formatting

        columns = get_table_structure(schema_name, table_name)

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


# Example usage (replace placeholders with your details)
statements = get_create_table_statements("public")
# print(statements)
if statements:
    # formatted_statements = [sqlformat(statement, reformat=True) for statement in statements]
    with open("../metadata.sql", "w") as outfile:
        outfile.writelines(statements)
    print("Formatted CREATE TABLE statements written to metadata.sql")
else:
    print("No tables found in schema")