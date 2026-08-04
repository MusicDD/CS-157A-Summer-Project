
"""
Install pip in order to run 
"""
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": "clubtime",
}

if not DB_CONFIG["password"]:
    raise RuntimeError(
        "DB_PASSWORD is not set. Create a .env file in the project root "
        "(copy .env.example and fill in your real password)."
    )


def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Could not connect to MySQL: {e}")
        raise