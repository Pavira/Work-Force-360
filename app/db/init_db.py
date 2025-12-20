import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Read DB info from environment
DB_HOST = os.getenv(
    "DB_HOST", "workforce360-database.c14u8ewuec90.ap-south-2.rds.amazonaws.com"
)
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "Pavithiran2310")
DB_NAME = os.getenv("DB_NAME", "workforce360_db")

conn = psycopg2.connect(
    dbname="postgres", user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (DB_NAME,))
exists = cur.fetchone()

if not exists:
    print(f"Database {DB_NAME} does not exist. Creating...")
    cur.execute(f"CREATE DATABASE {DB_NAME}")
else:
    print(f"Database {DB_NAME} already exists.")

cur.close()
conn.close()
