import os
from dotenv import load_dotenv
import mysql.connector
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_FILE = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_FILE, override=True)
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
if not DB_HOST:
    raise ValueError("DB_HOST was not loaded from .env")
try:
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = db.cursor()

except mysql.connector.Error as e:
    raise RuntimeError(
        f"Unable to connect to the MySQL database.\n\n"
        f"Please make sure MySQL is running and your .env settings are correct.\n\n"
        f"Database error: {e}"
    )
