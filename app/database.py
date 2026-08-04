import sqlite3
import os

DB_PATH = "database/backups.db"

os.makedirs("database", exist_ok=True)

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS backups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    backup_name TEXT,
    backup_date TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized successfully!")