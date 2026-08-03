
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

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Could not connect to MySQL: {e}")
        raise