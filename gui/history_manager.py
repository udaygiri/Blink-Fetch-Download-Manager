"""
History Manager

Saves and loads the history of downloads in a JSON file (downloads_history.json).
"""

import os
import json
from datetime import datetime
import shutil

_user_dir = os.path.join(os.path.expanduser("~"), ".blink_fetch_download_manager")
os.makedirs(_user_dir, exist_ok=True)
HISTORY_FILE = os.path.join(_user_dir, "downloads_history.json")

# Migration: copy existing local history to user folder if it exists
_local_history = "downloads_history.json"
if os.path.exists(_local_history) and not os.path.exists(HISTORY_FILE):
    try:
        
        shutil.copy2(_local_history, HISTORY_FILE)
    except Exception:
        pass


def load_history():
    """
    Loads all download records from the history file.

    Returns:
        list: A list of download records. Returns an empty list if there is no file or if an error happens.
    """
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []

def save_history(history):
    """
    Saves the list of downloads to the history file.

    Parameters:
        history (list): The list of download records to save.
    """
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
    except Exception:
        pass

def add_download_record(url, filename, filepath, size_str, total_bytes):
    """
    Adds a new download item to the history list.

    Parameters:
        url (str): The download link.
        filename (str): The name of the file.
        filepath (str): Where the file is saved on the computer.
        size_str (str): The size of the file as text.
        total_bytes (int): The size of the file in bytes.

    Returns:
        str: The unique ID created for this download item.
    """
    history = load_history()
    record_id = str(int(datetime.now().timestamp() * 1000))
    record = {
        "id": record_id,
        "url": url,
        "filename": filename,
        "filepath": filepath,
        "size": size_str,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Paused",
        "downloaded_bytes": 0,
        "total_bytes": total_bytes
    }
    history.insert(0, record)  # Add to the beginning
    save_history(history)
    return record_id

def update_download_status(record_id, status, downloaded_bytes=None, total_bytes=None):
    """
    Changes the status and downloaded bytes for a specific download item in history.

    Parameters:
        record_id (str): The unique ID of the download.
        status (str): The new status (like 'Downloading', 'Completed', 'Paused').
        downloaded_bytes (int, optional): How many bytes have been downloaded so far.
        total_bytes (int, optional): The total file size in bytes.
    """
    history = load_history()
    for record in history:
        if record["id"] == record_id:
            record["status"] = status
            if downloaded_bytes is not None:
                record["downloaded_bytes"] = downloaded_bytes
            if total_bytes is not None:
                record["total_bytes"] = total_bytes
            break
    save_history(history)

def delete_download_record(record_id):
    """
    Removes a download item from the history list.

    Parameters:
        record_id (str): The unique ID of the download to remove.
    """
    history = load_history()
    history = [r for r in history if r["id"] != record_id]
    save_history(history)
