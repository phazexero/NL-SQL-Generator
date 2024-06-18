# db/queries/queries.py
GET_ITEM_QUERY = """
    select * from ledgers where organization_id = :item_id
"""

GET_METADATA_QUERY = """
                        SELECT column_name, data_type, is_nullable, CHARACTER_MAXIMUM_LENGTH
                        FROM information_schema.columns
                        WHERE table_schema = :sname AND table_name = :tname;
                     """

GET_ALL_TABLE_NAMES = """
                        SELECT relname
                        FROM pg_stat_all_tables 
                        WHERE schemaname = 'public' 
                        ORDER BY relname;
                      """
