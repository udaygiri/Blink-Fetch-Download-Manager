"""
ChunkDownloader Module

This module handles downloading individual segments (chunks) of a file
using HTTP range requests. It allows multi-threaded segmented downloading
where each worker fetches and writes directly to a designated seek position
inside the target file.
"""

import requests
import threading

def download_chunk(url, thread_idx, chunks, filename, progress_bar, progress_callback=None, cancel_event=None, pause_event=None, save_meta_trigger=None):
    """
    Downloads a single file range segment on behalf of a designated worker thread.

    Parameters:
        url (str): The HTTP URL of the file to download.
        thread_idx (int): The index identifying this thread/worker.
        chunks (list): A list of dictionaries containing start, end, and current positions for all chunks.
        filename (str): The local destination file path to write the bytes to.
        progress_bar (tqdm): Optional tqdm console progress bar to update.
        progress_callback (callable): Optional callback function to execute with the size of each downloaded chunk.
        cancel_event (threading.Event): Event to monitor for immediate cancellation.
        pause_event (threading.Event): Event to monitor for thread execution suspension/resumption.
        save_meta_trigger (callable): Callback to trigger periodic progress commits to disk.
    """
    chunk_info = chunks[thread_idx]
    start = chunk_info["current"]
    end = chunk_info["end"]

    # If this chunk is already fully downloaded, return immediately
    if start > end:
        return

    header = {'Range': f'bytes={start}-{end}'}
    try:
        response = requests.get(url, headers=header, stream=True)
        if response.status_code not in [200, 206]:
            raise Exception(f"Server returned status code {response.status_code}")
    except Exception as e:
        raise e

    # Open file in read/write binary mode to write to seek position
    with open(filename, 'r+b') as file:
        file.seek(start)
        current_pos = start
        for chunk in response.iter_content(chunk_size=1024):
            if cancel_event is not None and cancel_event.is_set():
                break
            if pause_event is not None:
                pause_event.wait()
            if chunk:
                file.write(chunk)
                current_pos += len(chunk)
                chunk_info["current"] = current_pos
                
                if progress_bar:
                    progress_bar.update(len(chunk))
                if progress_callback is not None:
                    progress_callback(len(chunk))
                if save_meta_trigger is not None:
                    save_meta_trigger()
