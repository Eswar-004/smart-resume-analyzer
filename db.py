import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("MYSQLHOST") or os.getenv("DB_HOST"),
        port=int(os.getenv("MYSQLPORT") or os.getenv("DB_PORT", 3306)),
        user=os.getenv("MYSQLUSER") or os.getenv("DB_USER"),
        password=os.getenv("MYSQLPASSWORD") or os.getenv("DB_PASSWORD"),
        database=os.getenv("MYSQLDATABASE") or os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )