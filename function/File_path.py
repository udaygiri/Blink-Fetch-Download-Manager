"""
File_path Module

This module manages filename sanitization, remote content-disposition header
parsing to determine valid file names, mime-type extension fallback guessing,
and organization of local files into categorized subfolders (e.g., Compressed,
Pictures, Videos, Music, Documents, Executables, Code).
"""

import re
from datetime import datetime
import os
import requests
import mimetypes
from email.header import decode_header
from urllib.parse import unquote

# Custom extension categories
EXTENSIONS = {
    "Compressed": (".zip", ".tar", ".tar.gz", ".rar", ".7z", ".gz", ".bz2", ".xz", ".iso"),
    "Pictures": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico", ".heic", ".avif"),
    "Videos": (".mp4", ".mkv", ".avi", ".mov", ".wmv", ".flv", ".webm", ".3gp", ".mpeg", ".mpg", ".m4v"),
    "Music": (".mp3", ".wav", ".aac", ".flac", ".ogg", ".wma", ".m4a", ".opus", ".mid", ".amr"),
    "Documents": (".pdf", ".epub", ".mobi", ".txt", ".doc", ".docx", ".odt", ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".rtf", ".tex", ".md"),
    "Executables": (".exe", ".msi", ".apk", ".bat", ".sh", ".bin", ".dmg", ".jar", ".appimage"),
    "Code": (".py", ".java", ".cpp", ".c", ".cs", ".html", ".htm", ".css", ".js", ".ts", ".php", ".rb", ".go", ".rs", ".swift", ".kt", ".sql", ".xml", ".json", ".yaml", ".yml", ".ini"),
    "Others": ()  # fallback
}

def get_category(filename):
    """
    Identifies the download folder category name for the specified filename extension.

    Parameters:
        filename (str): The filename.

    Returns:
        str: The matching category key from EXTENSIONS dictionary, or "Others" as fallback.
    """
    ext = os.path.splitext(filename)[1].lower()
    for category, extensions in EXTENSIONS.items():
        if ext in extensions:
            return category
    return "Others"

def sanitize_filename(filename):
    """
    Cleans the given filename string to make it safe for file systems (especially Windows).
    Removes query strings, unquotes URL encoding, strips invalid characters, and trims whitespace.

    Parameters:
        filename (str): The raw string representing the filename.

    Returns:
        str: The sanitized filename.
    """
    # Unquote URL-encoded characters (like %20 -> space)
    filename = unquote(filename)
    # Remove query parameters and anchors
    filename = filename.split('?')[0].split('#')[0]
    # Replace invalid characters for Windows filenames: < > : " / \ | ? *
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Strip leading/trailing spaces and periods
    filename = filename.strip(' .')
    return filename

def file_path(url):
    """
    Requests headers from the target URL, extracts the filename (using Content-Disposition
    or splitting the URL), sanitizes it, resolves extensions using mimetypes if needed,
    categorizes it, and builds the full local download path.

    Parameters:
        url (str): The source URL.

    Returns:
        str: The resolved, absolute or relative local download path.
    """
    # Send a HEAD request to get the headers (or use GET if HEAD is not supported)
    response = requests.head(url, allow_redirects=True)

    # If HEAD is not supported, use GET (but don't download the content)
    if response.status_code != 200:
        response = requests.get(url, stream=True, allow_redirects=True)

    content_disposition = response.headers.get('Content-Disposition')
    filename = None
    if content_disposition:
        # Use regex to extract filename or filename* (RFC 6266)
        fname_match = re.search(r"filename\*?=(?:UTF-8''|\"|')?([^;\"']+)", content_disposition, re.IGNORECASE)
        if fname_match:
            filename = fname_match.group(1)
            # Decode RFC 2047 encoded filenames if present
            if filename.startswith('=?') and filename.endswith('?='):
                decoded_parts = decode_header(filename)
                filename = ''.join([
                    part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
                    for part, encoding in decoded_parts
                ])
    if not filename:
        # Extract filename from URL
        filename = url.split("/")[-1]

    # Sanitize the filename early
    filename = sanitize_filename(filename)

    # Guess extension from content-type if missing
    content_type = response.headers.get("content-type", "")
    guessed_ext = mimetypes.guess_extension(content_type.split(";")[0].strip()) if content_type else None

    if not os.path.splitext(filename)[1] and guessed_ext:
        filename += guessed_ext
    elif not os.path.splitext(filename)[1]:
        filename = f"file_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.bin"

    # Get category folder
    category = get_category(filename)
    # Locate user's system Downloads folder and save under "Downloads/Blink Fetch/[Category]/[Filename]"
    system_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    base_download_dir = os.path.join(system_downloads, "Blink Fetch")
    filepath = os.path.join(base_download_dir, category, filename)

    # Ensure folder exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    return filepath
