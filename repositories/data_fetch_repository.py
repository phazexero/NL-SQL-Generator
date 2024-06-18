# db/repositories/print_settings_repository.py
from databases import Database
from config.db.queries import GET_ITEM_QUERY
from config.db.queries import GET_METADATA_QUERY
from config.db.queries import GET_ALL_TABLE_NAMES

async def get_item(db: Database, item_id: int):
    return await db.fetch_all(GET_ITEM_QUERY, values={"item_id": item_id})

async def get_metadata(db: Database, sname: str, tname: str):
    return await db.fetch_all(GET_METADATA_QUERY, values={"sname": sname, "tname": tname})

async def get_names(db: Database):
    return await db.fetch_all(GET_ALL_TABLE_NAMES)
