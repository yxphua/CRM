import sqlite3

def get_connection():
    return sqlite3.connect("crm.db")

def setup_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            MemberId INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            points INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            TransId INTEGER PRIMARY KEY AUTOINCREMENT,
            MemberId INTEGER,
            amount REAL,
            datetime TEXT,
            FOREIGN KEY (MemberId) REFERENCES members(MemberId)
        )
    """)

    cursor.execute(
        "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
        ("admin", "1234")
    )

    conn.commit()
    conn.close()
