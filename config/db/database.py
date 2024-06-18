# db/database.py
import os
from databases import Database
from sqlalchemy import create_engine, MetaData
from urllib.parse import quote
from dotenv import load_dotenv

load_dotenv()

# Read database credentials from environment variables
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("DB_USER", "user")
DB_NAME = os.environ.get("DB_NAME", "dbname")

# URL-encode the password
ENCODED_DB_PASS = quote(os.environ.get("DB_PASS", "password"), safe="")

# Construct the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{ENCODED_DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

database = Database(DATABASE_URL)

class DatabaseSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls)
            cls._instance._init_database()
        return cls._instance

    def _init_database(self):
        self.database = Database(DATABASE_URL)
        self.metadata = MetaData()
        engine = create_engine(DATABASE_URL)
        self.metadata.create_all(bind=engine)


async def get_database():
    database_singleton = DatabaseSingleton()
    try:
        # Ensure the database is connected
        await database_singleton.database.connect()
        yield database_singleton.database
    finally:
        # Ensure the database is disconnected
        await database_singleton.database.disconnect()
