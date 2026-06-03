import os
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '2889'),
        database=os.getenv('DB_NAME', 'project'),
        cursorclass=pymysql.cursors.DictCursor
    )