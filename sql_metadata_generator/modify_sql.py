def modify_sql(sql_file):
    with open(sql_file, 'r') as f:
        sql_content = f.read()

    statements = sql_content.split(';')  # Split into individual statements
    modified_statements = []
    for statement in statements:
        if statement.strip():  # Skip empty statements
            lines = statement.splitlines()  # Split into lines
            modified_lines = []
            for line in lines:
                if 'character varying' in line:
                    modified_line = line.replace('character varying', 'CHARACTER VARYING(255)')
                else:
                    modified_line = line
                modified_lines.append(modified_line)
            modified_statements.append('\n'.join(modified_lines))
    return ';'.join(modified_statements)

# Example usage
sql_file = 'schema_statements_formatted.sql'
modified_sql = modify_sql(sql_file)

# Print or write the modified SQL content
# print(modified_sql)

# You can also write the modified content to a new file
with open('modified_sql_file.sql', 'w') as f:
  f.write(modified_sql)
  