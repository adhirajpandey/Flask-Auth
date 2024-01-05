import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

 
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def connect_pg():
    try:
        conn = psycopg2.connect(database=DB_NAME,user=DB_USER,password=DB_PASS,
                                host=DB_HOST,port=DB_PORT)
        return conn
    except:
        print("unable to connect to the database")
        return None
    
conn = connect_pg()

def create_table():
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT, password TEXT)")
    conn.commit()
    cursor.close()

def insert_username_password_admin(username: str, password: str, admin: bool = False):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, admin) VALUES (%s, %s, %s)", (username, password, admin))
    conn.commit()
    cursor.close()

def fetch_all_users():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    return rows

def fetch_user_by_username(username: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    rows = cursor.fetchone()
    cursor.close()
    return rows

def check_if_username_exists(username: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    rows = cursor.fetchone()
    cursor.close()
    if rows:
        return True
    else:
        return False

def check_if_admin(username: str):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    rows = cursor.fetchone()
    cursor.close()
    if rows[3]:
        return True
    else:
        return False


