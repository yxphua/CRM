import sqlite3

def get_connection():
    return sqlite3.connect("crm.db")

def setup_database():
    with get_connection() as conn:
        cursor = conn.cursor()

        #Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)

        #Create members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                MemberId INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE NOT NULL,
                points INTEGER DEFAULT 0
            )
        """)

        #Create transactions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                TransId INTEGER PRIMARY KEY AUTOINCREMENT,
                MemberId INTEGER,
                amount REAL CHECK(amount >= 0),
                datetime TEXT,
                FOREIGN KEY (MemberId) REFERENCES members(MemberId)
            )
        """)
        
        import hashlib
        hashed_pwd = hashlib.sha256("1234".encode()).hexdigest()
    
        #Insert default admin user
        cursor.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            ("admin", hashed_pwd)
        )