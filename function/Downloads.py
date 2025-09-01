import requests
import threading
from tqdm import tqdm
from datetime import datetime
from .File_path import file_path

def download_chunk(url, start, end, filename, progress_bar, progress_callback=None):

    header = {'Range': f'bytes={start}-{end}'}
    response = requests.get(url, headers=header, stream=True)
    with open(filename, 'r+b') as file:
        file.seek(start)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                if progress_bar:
                    progress_bar.update(len(chunk))
                if progress_callback is not None:
                    progress_callback(len(chunk))
    

def get_file_size(url):

    response = requests.head(url)
    return int(response.headers.get('content-length', 0))

def download_file(url, num_threads=4, progress_callback=None):

    if url is None:
        raise ValueError("URL must be provided")

    filename = file_path(url)
    file_size = get_file_size(url)
    chunk_size = file_size // num_threads

    print("-" * 50)
    print("Starting download...")
    print("-" * 50)
    print(f"File Name: {filename}")
    print("-" * 50)
    print(f"File Size: {file_size/1e6} MB")
    print("-" * 50)

    with open(filename, 'wb') as file:
        file.write(b'\0' * file_size)

    progress_bar = tqdm(total=file_size, unit='B', unit_scale=True, desc=filename) if progress_callback is None else None
    downloaded = [0]
    def gui_progress_callback(bytes_downloaded):
        downloaded[0] += bytes_downloaded
        if progress_callback is not None:
            progress_callback(downloaded[0], file_size)
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = start + chunk_size - 1 if i < num_threads - 1 else file_size - 1
        thread = threading.Thread(
            target=download_chunk,
            args=(url, start, end, filename, progress_bar, gui_progress_callback if progress_callback is not None else None)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    if progress_bar:
        progress_bar.close()
    print(f"Download completed: {filename}")
    print("-" * 50)
