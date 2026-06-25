"""
Downloads Orchestrator Module

This is the main entry point for starting, partitions scheduling, and coordinating
segmented multi-threaded file downloads. It manages loading previous resume states,
allocating file sizes, dispatching worker threads, and triggering speed/completion callbacks.
"""

import threading
import time
import os
from tqdm import tqdm
from .File_path import file_path
from .ResumeManager import load_metadata, save_metadata, delete_metadata
from .SizeHelper import get_file_size
from .ChunkDownloader import download_chunk

def download_file(url, num_threads=4, progress_callback=None, filepath=None, cancel_event=None, pause_event=None):
    """
    Orchestrates the download of a file using multi-threading with range requests.
    Attempts to resume from an existing metadata file if found.

    Parameters:
        url (str): The HTTP URL of the file to download.
        num_threads (int): The number of concurrent threads to use (default 4).
        progress_callback (callable): Optional callback triggered with (downloaded_bytes, total_bytes).
        filepath (str): The destination path. If None, it is determined automatically.
        cancel_event (threading.Event): Event to cancel the download process.
        pause_event (threading.Event): Event to pause/resume the download process.
    """
    if url is None:
        raise ValueError("URL must be provided")

    if filepath is None:
        filename = file_path(url)
    else:
        filename = filepath

    file_size = get_file_size(url)

    # Check for existing metadata (if file also exists)
    metadata = load_metadata(filename)
    
    # Calculate downloaded bytes if resuming
    initial_downloaded = 0
    if metadata and os.path.exists(filename) and metadata.get("file_size") == file_size:
        chunks = metadata.get("chunks")
        # Adjust threads count to whatever the metadata has
        num_threads = len(chunks)
        for chunk in chunks:
            initial_downloaded += (chunk["current"] - chunk["start"])
        print("-" * 50)
        print("Resuming previous download...")
    else:
        # Pre-allocate blank file
        with open(filename, 'wb') as file:
            file.write(b'\0' * file_size)

        # Create new chunks partition
        chunk_size = file_size // num_threads
        chunks = []
        for i in range(num_threads):
            start = i * chunk_size
            end = start + chunk_size - 1 if i < num_threads - 1 else file_size - 1
            chunks.append({
                "start": start,
                "end": end,
                "current": start
            })
        # Save initial progress metadata
        save_metadata(filename, url, file_size, chunks)

    print("-" * 50)
    print("Starting download...")
    print("-" * 50)
    print(f"File Name: {filename}")
    print("-" * 50)
    print(f"File Size: {file_size/1e6:.2f} MB")
    print("-" * 50)

    progress_bar = tqdm(total=file_size, initial=initial_downloaded, unit='B', unit_scale=True, desc=filename) if progress_callback is None else None
    
    # Track downloaded bytes
    downloaded = [initial_downloaded]
    last_update_time = [0.0]
    last_meta_save_time = [0.0]
    
    lock = threading.Lock()
    meta_lock = threading.Lock()

    def gui_progress_callback(bytes_downloaded):
        with lock:
            downloaded[0] += bytes_downloaded
            current_downloaded = downloaded[0]
            now = time.time()
            if now - last_update_time[0] >= 0.1 or current_downloaded >= file_size:
                last_update_time[0] = now
                should_update = True
            else:
                should_update = False
        
        if should_update and progress_callback is not None:
            progress_callback(current_downloaded, file_size)

    def save_meta_trigger():
        now = time.time()
        with meta_lock:
            if now - last_meta_save_time[0] >= 1.0:
                last_meta_save_time[0] = now
                save_metadata(filename, url, file_size, chunks)

    threads = []
    thread_errors = []

    # Wrapper to capture thread exceptions
    def run_thread(t_idx):
        try:
            download_chunk(
                url,
                t_idx,
                chunks,
                filename,
                progress_bar,
                gui_progress_callback,
                cancel_event,
                pause_event,
                save_meta_trigger
            )
        except Exception as e:
            thread_errors.append(e)

    for i in range(num_threads):
        thread = threading.Thread(target=run_thread, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if progress_bar:
        progress_bar.close()

    # Raise thread errors if any occurred
    if thread_errors:
        raise thread_errors[0]

    # Clean up metadata file if completed successfully
    if not (cancel_event and cancel_event.is_set()):
        delete_metadata(filename)
        print(f"Download completed: {filename}")
        print("-" * 50)
