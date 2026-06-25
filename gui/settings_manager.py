"""
Settings Manager Utility

Handles reading and writing the application settings configuration preferences
from settings_config.json.
"""

import os
import json

_user_dir = os.path.join(os.path.expanduser("~"), ".blink_fetch_download_manager")
os.makedirs(_user_dir, exist_ok=True)
SETTINGS_FILE = os.path.join(_user_dir, "settings_config.json")

# Migration: copy existing local settings to user folder if it exists
_local_settings = "settings_config.json"
if os.path.exists(_local_settings) and not os.path.exists(SETTINGS_FILE):
    try:
        import shutil
        shutil.copy2(_local_settings, SETTINGS_FILE)
    except Exception:
        pass


def load_settings():
    """
    Loads saved configurations from settings_config.json.

    Returns:
        dict: The config dictionary, or empty dict if not found/invalid.
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_settings(threads, theme):
    """
    Persists configuration settings to settings_config.json.

    Parameters:
        threads (str): Selected count of download threads.
        theme (str): Active appearance mode name.
    """
    config = {
        "threads": threads,
        "theme": theme
    }
    try:
        with open(SETTINGS_FILE, "w") as f:
            json.dump(config, f)
    except Exception:
        pass
