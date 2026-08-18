import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")
GITHUB_REPO = os.getenv("GITHUB_REPO")

GITHUB_API_URL = (
    f"https://api.github.com/repos/"
    f"{GITHUB_OWNER}/{GITHUB_REPO}/contents"
)


def upload_backup(file_path):

    # Check environment variables
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN is missing from .env")
        return

    if not GITHUB_OWNER:
        print("ERROR: GITHUB_OWNER is missing from .env")
        return

    if not GITHUB_REPO:
        print("ERROR: GITHUB_REPO is missing from .env")
        return

    # Check backup file
    if not os.path.exists(file_path):
        print(f"ERROR: Backup file not found: {file_path}")
        return

    file_name = os.path.basename(file_path)

    print(f"Uploading: {file_path}")

    # Read backup file
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode("utf-8")

    # GitHub storage path
    github_path = f"cloud_backups/{file_name}"

    url = f"{GITHUB_API_URL}/{github_path}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # ------------------------------------------------
    # Check whether the file already exists
    # ------------------------------------------------

    check_response = requests.get(
        url,
        headers=headers
    )

    data = {
        "message": f"Upload backup {file_name}",
        "content": content
    }

    # If file already exists, get its SHA
    if check_response.status_code == 200:

        existing_file = check_response.json()

        data["sha"] = existing_file["sha"]

        print("Existing backup found.")
        print("Updating backup on GitHub...")

    elif check_response.status_code == 404:

        print("New backup file.")
        print("Creating backup on GitHub...")

    else:

        print("Could not check GitHub file.")

        print(
            f"Status code: "
            f"{check_response.status_code}"
        )

        print(
            f"Response: "
            f"{check_response.text}"
        )

        return

    # ------------------------------------------------
    # Upload / update file
    # ------------------------------------------------

    response = requests.put(
        url,
        headers=headers,
        json=data
    )

    if response.status_code in [200, 201]:

        print()
        print("======================================")
        print("GitHub upload successful!")
        print("======================================")
        print(f"GitHub file: {github_path}")

    else:

        print()
        print("GitHub upload failed!")
        print()
        print(f"Status code: {response.status_code}")
        print()
        print(f"Response: {response.text}")


# ------------------------------------------------
# Main program
# ------------------------------------------------

if __name__ == "__main__":

    backup_folder = "backups"

    # Find all ZIP backup files
    backup_files = [
        os.path.join(backup_folder, file)
        for file in os.listdir(backup_folder)
        if file.endswith(".zip")
    ]

    if not backup_files:

        print("No backup files found.")

    else:

        # Select latest backup
        latest_backup = max(
            backup_files,
            key=os.path.getmtime
        )

        upload_backup(latest_backup)