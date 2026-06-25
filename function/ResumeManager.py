"""
ResumeManager Module

This module manages the saving, loading, and deletion of download progress metadata
to support pausing and resuming files. Metadata is stored in a clean, isolated
'temp' directory in the workspace using unique file path hashes.
"""

import os
import json
import hashlib

# Directory to save all temporary .blink resume config files
TEMP_DIR = os.path.abspath("temp")
os.makedirs(TEMP_DIR, exist_ok=True)

def get_metadata_path(filepath):
    """
    Generates a unique file path for the metadata config based on the absolute
    local file path's MD5 hash.

    Parameters:
        filepath (str): The local target destination path.

    Returns:
        str: The absolute path to the .blink config file.
    """
    path_hash = hashlib.md5(os.path.abspath(filepath).encode()).hexdigest()
    return os.path.join(TEMP_DIR, f"{path_hash}.blink")

def load_metadata(filepath):
    """
    Loads saved chunk pointers for the specified download destination if they exist.

    Parameters:
        filepath (str): The local destination file path.

    Returns:
        dict: The loaded metadata dictionary or None if not found/corrupted.
    """
    meta_path = get_metadata_path(filepath)
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return None

def save_metadata(filepath, url, file_size, chunks):
    """
    Saves the current download session progress (chunk pointers) to the temp directory.

    Parameters:
        filepath (str): The target file destination path.
        url (str): The download source URL.
        file_size (int): The total file length in bytes.
        chunks (list): List of dictionaries containing start, end, and current positions of threads.
    """
    meta_path = get_metadata_path(filepath)
    data = {
        "url": url,
        "filepath": os.path.abspath(filepath),
        "file_size": file_size,
        "chunks": chunks
    }
    try:
        with open(meta_path, "w") as f:
            json.dump(data, f, indent=4)
    except Exception:
        pass

def delete_metadata(filepath):
    """
    Cleans up and deletes the temporary session metadata file when a download
    completes successfully or is deleted.

    Parameters:
        filepath (str): The target file path.
    """
    meta_path = get_metadata_path(filepath)
    if os.path.exists(meta_path):
        try:
            os.remove(meta_path)
        except Exception:
            pass
