import os

from dotenv import load_dotenv
from psycopg_pool import ConnectionPool

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": os.getenv("POSTGRES_PORT", "5433"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "connect_timeout": 5,
}

pool = ConnectionPool(
    kwargs=DB_CONFIG,
    min_size=1,
    max_size=10,
    timeout=5,
    open=False,
)
