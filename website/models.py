import sqlite3


def init_db():
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                phone TEXT,
                points INTEGER DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()

def get_user_by_email(email):
        conn = sqlite3.connect('users.db')
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        return user

def add_user(name, email, password, phone):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (name, email, password, phone) VALUES (?, ?, ?, ?)', 
                  (name, email, password, phone))
        conn.commit()
        conn.close()