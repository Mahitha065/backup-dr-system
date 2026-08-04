import shutil
import os
import sqlite3
from datetime import datetime

SOURCE_FOLDER = "test_data"
BACKUP_FOLDER = "backups"

os.makedirs(BACKUP_FOLDER, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

backup_name = f"backup_{timestamp}"
backup_path = os.path.join(BACKUP_FOLDER, backup_name)

shutil.make_archive(
    backup_path,
    "zip",
    SOURCE_FOLDER
)

conn = sqlite3.connect("database/backups.db")
cursor = conn.cursor()

cursor.execute(
    """
    INSERT INTO backups
    (backup_name, backup_date, status)
    VALUES (?, ?, ?)
    """,
    (
        f"{backup_name}.zip",
        timestamp,
        "SUCCESS"
    )
)

conn.commit()
conn.close()

print("Backup created successfully!")
print(f"Location: {backup_path}.zip")