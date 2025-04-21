import sqlite3

conn = sqlite3.connect("booksmart.db")
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()

print("Tables in booksmart.db:")
for table in tables:
    print(table[0])

conn.close()
