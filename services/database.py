# services/database.py
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def get_db():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASS", ""),
            database=os.getenv("DB_NAME", "rios_pastries")
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return None