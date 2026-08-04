import zipfile
import os

BACKUP_FILE = "backups"

RESTORE_FOLDER = "restored_files"

os.makedirs(RESTORE_FOLDER, exist_ok=True)

files = os.listdir(BACKUP_FILE)

zip_files = [f for f in files if f.endswith(".zip")]

if not zip_files:
    print("No backup files found.")
else:
    latest_backup = sorted(zip_files)[-1]

    with zipfile.ZipFile(
        os.path.join(BACKUP_FILE, latest_backup),
        "r"
    ) as zip_ref:
        zip_ref.extractall(RESTORE_FOLDER)

    print("Restore completed successfully!")