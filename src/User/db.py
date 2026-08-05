import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME", "clubtime"),
}

if not DB_CONFIG["password"]:
    raise RuntimeError(
        "DB_PASSWORD is not set. Create a .env file in the project root "
        "(copy .env.example and fill in your real password)."
    )


def get_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        print(f"Could not connect to MySQL: {e}")
        raise