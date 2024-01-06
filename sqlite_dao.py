import sqlite3


DB_FILE_PATH = "database.db"


def connect_sqlite():
    try:
        conn = sqlite3.connect(DB_FILE_PATH)
        return conn
    except:
        print("Unable to connect to the database")
        return None


conn = connect_sqlite()


def create_table():
    conn = connect_sqlite()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, admin INTEGER)")
    conn.commit()
    cursor.close()
    conn.close()

def insert_username_password_admin(username: str, password: str, admin: bool = False):
    conn = connect_sqlite()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password, admin) VALUES (?, ?, ?)", (username, password, int(admin)))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_all_users():
    conn = connect_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def fetch_user_by_username(username: str):
    conn = connect_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    rows = cursor.fetchone()
    cursor.close()
    conn.close()
    return rows

def check_if_username_exists(username: str):
    conn = connect_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    rows = cursor.fetchone()
    cursor.close()
    conn.close()
    if rows:
        return True
    else:
        return False

def check_if_admin(username: str):
    conn = connect_sqlite()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    rows = cursor.fetchone()
    cursor.close()
    conn.close()
    if rows and rows[3]:
        return True
    else:
        return False


create_table()