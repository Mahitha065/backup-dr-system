import os
import zipfile
from datetime import datetime
import sqlite3

from github_backup import upload_backup


# ==============================
# PROJECT PATHS
# ==============================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SOURCE_FOLDER = os.path.join(BASE_DIR, "test_data")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backups")
DATABASE_FOLDER = os.path.join(BASE_DIR, "database")
DATABASE_PATH = os.path.join(DATABASE_FOLDER, "backups.db")


# ==============================
# CREATE REQUIRED FOLDERS
# ==============================

os.makedirs(SOURCE_FOLDER, exist_ok=True)
os.makedirs(BACKUP_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)


# ==============================
# INITIALIZE DATABASE
# ==============================

def initialize_database():

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# ==============================
# SAVE BACKUP HISTORY
# ==============================

def save_backup_history(filename, timestamp, status):

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO backups
        (filename, timestamp, status)
        VALUES (?, ?, ?)
    """, (filename, timestamp, status))

    connection.commit()
    connection.close()


# ==============================
# CREATE ZIP BACKUP
# ==============================

def create_backup():

    print("\n==============================")
    print("BACKUP PROCESS STARTED")
    print("==============================")

    # Create unique backup name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_filename = f"backup_{timestamp}.zip"

    backup_path = os.path.join(
        BACKUP_FOLDER,
        backup_filename
    )

    # Create ZIP file
    try:

        with zipfile.ZipFile(
            backup_path,
            "w",
            zipfile.ZIP_DEFLATED
        ) as zip_file:

            for root, directories, files in os.walk(SOURCE_FOLDER):

                for file in files:

                    file_path = os.path.join(root, file)

                    # Store files inside ZIP without full computer path
                    relative_path = os.path.relpath(
                        file_path,
                        SOURCE_FOLDER
                    )

                    zip_file.write(
                        file_path,
                        relative_path
                    )

        print("\nBackup created successfully!")
        print("Local location:")
        print(backup_path)

    except Exception as error:

        print("\nBackup creation failed!")
        print("Error:", error)

        save_backup_history(
            backup_filename,
            timestamp,
            "FAILED"
        )

        return


    # ==============================
    # SAVE SUCCESS TO DATABASE
    # ==============================

    save_backup_history(
        backup_filename,
        timestamp,
        "SUCCESS"
    )

    print("\nBackup history saved to database.")


    # ==============================
    # UPLOAD TO GITHUB
    # ==============================

    print("\nUploading backup to GitHub...")

    print("\nUploading backup to GitHub...")
    
    upload_backup(backup_path)
    print("\nGitHub upload process completed.")

    print("\n==============================")
    print("BACKUP PROCESS COMPLETED")
    print("==============================")


# ==============================
# PROGRAM START
# ==============================

if __name__ == "__main__":

    initialize_database()

    create_backup()