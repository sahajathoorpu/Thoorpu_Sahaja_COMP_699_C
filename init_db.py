import sqlite3


def init_db():
    conn = sqlite3.connect("booksmart.db")
    cur = conn.cursor()

    # Create users table
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            phone TEXT,
            points INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
