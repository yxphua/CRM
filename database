import sqlite3

def get_connection():
    return sqlite3.connect("crm.db")

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    # Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT
        )
    """)

    # Example login account
    cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
                   ("admin", "1234"))

    conn.commit()
    conn.close()
