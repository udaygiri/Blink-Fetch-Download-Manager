"""
GUI Formatting Utilities

Provides utility functions to format sizes and speeds into human-readable strings.
"""

def format_speed(speed_bytes_per_sec):
    """
    Formats raw speed count in bytes/second into a human-readable string.

    Parameters:
        speed_bytes_per_sec (float): Raw speed in bytes per second.

    Returns:
        str: Format matched string (e.g. "2.40 MB/s", "120.40 KB/s", "80 B/s").
    """
    if speed_bytes_per_sec >= 1024 * 1024:
        return f"{speed_bytes_per_sec / (1024 * 1024):.2f} MB/s"
    elif speed_bytes_per_sec >= 1024:
        return f"{speed_bytes_per_sec / 1024:.2f} KB/s"
    else:
        return f"{speed_bytes_per_sec:.2f} B/s"

def format_size(size_bytes):
    """
    Formats raw byte count into a human-readable string.

    Parameters:
        size_bytes (int): Size in bytes.

    Returns:
        str: Format matched string (e.g. "1.50 GB", "45.20 MB", "12 KB", "50 B").
    """
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    else:
        return f"{size_bytes} B"
