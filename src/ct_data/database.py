import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Automatically load key-value pairs from .env into system environment variables
load_dotenv()

def get_db_engine():
    """Reads credentials from .env and returns a SQLAlchemy Engine."""
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")

    # Validate that essential credentials exist
    if not user or not password or not db_name:
        raise ValueError("Missing database credentials in .env file!")

    database_url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return create_engine(database_url)