"""
SizeHelper Module

Provides utility functions to contact remote HTTP servers and determine the
total content length/size of files before the download starts.
"""

import requests

def get_file_size(url):
    """
    Retrieves the total size of the file at the specified URL in bytes.
    Sends a HEAD request first, and falls back to a stream GET request if the server
    does not support HEAD requests.

    Parameters:
        url (str): The HTTP URL of the file.

    Returns:
        int: The size of the file in bytes, or 0 if the size could not be retrieved.
    """
    response = requests.head(url, allow_redirects=True)
    if response.status_code != 200:
        response = requests.get(url, stream=True, allow_redirects=True)
    return int(response.headers.get('content-length', 0))
