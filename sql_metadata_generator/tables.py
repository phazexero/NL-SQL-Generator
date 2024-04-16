import psycopg2

def get_table_names(host, port, database, user, password):
    schema_name = "public"
    try:
        conn = psycopg2.connect(
                    host=host,
                    port = port,
                    database=database,
                    user=user,
                    password=password
                )
        cursor = conn.cursor()

        # Execute query to get table names
        cursor.execute("""
                       select relname
                        from pg_stat_all_tables 
                        WHERE schemaname = 'public' 
                        ORDER BY relname;
                        """, (schema_name,))

        # Fetch all table names
        table_names = [row[0] for row in cursor.fetchall()]

    except Exception as e:
        print(f"Error getting table names: {e}")
        return []

    finally:
        if conn:
            cursor.close()
            conn.close()

    tables = []
    if table_names:
        print("Tables in schema", schema_name, ":")
        for table in table_names:
            tables.append(table)
    # print(tables)
    return tables
