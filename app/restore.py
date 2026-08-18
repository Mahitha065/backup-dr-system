import os
import base64
import zipfile
import requests
from dotenv import load_dotenv


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

RESTORE_FOLDER = os.path.join(
    BASE_DIR,
    "restored_files"
)


# ==========================================
# GITHUB API
# ==========================================

GITHUB_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_OWNER}/{GITHUB_REPO}/contents/cloud_backups"
)


HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}


# ==========================================
# LIST BACKUPS
# ==========================================

def list_backups():

    print("\n======================================")
    print("AVAILABLE BACKUPS")
    print("======================================")

    response = requests.get(
        GITHUB_URL,
        headers=HEADERS
    )

    if response.status_code != 200:

        print("Could not retrieve backups.")

        print("Status code:", response.status_code)

        print("Response:", response.text)

        return []

    files = response.json()

    backups = []

    for file in files:

        if file["name"].endswith(".zip"):

            backups.append(file)

    if not backups:

        print("No backup files found on GitHub.")

        return []

    for index, backup in enumerate(backups, start=1):

        print(
            f"{index}. {backup['name']}"
        )

    return backups


# ==========================================
# DOWNLOAD BACKUP
# ==========================================

def download_backup(backup):

    print("\n======================================")
    print("DOWNLOADING BACKUP")
    print("======================================")

    file_url = backup["download_url"]

    response = requests.get(
        file_url,
        headers=HEADERS
    )

    if response.status_code != 200:

        print("Backup download failed.")

        print(
            "Status code:",
            response.status_code
        )

        return None

    temporary_zip = os.path.join(
        BASE_DIR,
        backup["name"]
    )

    with open(
        temporary_zip,
        "wb"
    ) as file:

        file.write(response.content)

    print(
        "Backup downloaded successfully."
    )

    print(
        "Downloaded file:",
        temporary_zip
    )

    return temporary_zip


# ==========================================
# RESTORE BACKUP
# ==========================================

def restore_backup(zip_path):

    print("\n======================================")
    print("RESTORING BACKUP")
    print("======================================")

    os.makedirs(
        RESTORE_FOLDER,
        exist_ok=True
    )

    try:

        with zipfile.ZipFile(
            zip_path,
            "r"
        ) as zip_file:

            zip_file.extractall(
                RESTORE_FOLDER
            )

        print(
            "Backup extracted successfully!"
        )

        print(
            "Restored location:",
            RESTORE_FOLDER
        )

        return True

    except Exception as error:

        print(
            "Restore failed!"
        )

        print(
            "Error:",
            error
        )

        return False


# ==========================================
# MAIN RESTORE PROCESS
# ==========================================

def main():

    print("\n")
    print("======================================")
    print("   DISASTER RECOVERY SYSTEM")
    print("======================================")

    # Check environment variables

    if not GITHUB_TOKEN:

        print("ERROR: GITHUB_TOKEN missing.")

        return

    if not GITHUB_OWNER:

        print("ERROR: GITHUB_OWNER missing.")

        return

    if not GITHUB_REPO:

        print("ERROR: GITHUB_REPO missing.")

        return


    # Get backups

    backups = list_backups()

    if not backups:

        return


    # Ask user to select backup

    while True:

        try:

            choice = int(
                input(
                    "\nEnter backup number to restore: "
                )
            )

            if 1 <= choice <= len(backups):

                selected_backup = backups[
                    choice - 1
                ]

                break

            else:

                print(
                    "Invalid number. Try again."
                )

        except ValueError:

            print(
                "Please enter a number."
            )


    print(
        "\nSelected backup:",
        selected_backup["name"]
    )


    # Download

    zip_path = download_backup(
        selected_backup
    )

    if not zip_path:

        return


    # Restore

    success = restore_backup(
        zip_path
    )


    # Delete temporary ZIP

    if os.path.exists(zip_path):

        os.remove(zip_path)


    # Final result

    print("\n======================================")

    if success:

        print(
            "DISASTER RECOVERY SUCCESSFUL!"
        )

    else:

        print(
            "DISASTER RECOVERY FAILED!"
        )

    print("======================================")


# ==========================================
# START PROGRAM
# ==========================================

if __name__ == "__main__":

    main()