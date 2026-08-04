import sqlite3

conn = sqlite3.connect("database/backups.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM backups")

rows = cursor.fetchall()

print("\nBACKUP HISTORY\n")

for row in rows:
    print(row)

conn.close()