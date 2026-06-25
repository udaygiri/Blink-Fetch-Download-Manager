"""
Download Backend Thread

Contains the background thread that runs the download process in the background.
"""

import threading
from function.Downloads import download_file

class DownloadThread(threading.Thread):
    """
    A thread that runs the download file function in the background
    so the app window does not freeze.
    """
    def __init__(self, url, filepath, progress_callback, error_callback, cancel_event, pause_event, num_threads=4):
        """
        Initializes the DownloadThread.

        Parameters:
            url (str): The download link of the file.
            filepath (str): Where to save the file on the computer.
            progress_callback (callable): Function to run to show progress updates.
            error_callback (callable): Function to run if something goes wrong.
            cancel_event (threading.Event): Event to stop the download.
            pause_event (threading.Event): Event to pause or resume the download.
            num_threads (int): How many threads to use.
        """
        super().__init__()
        self.url = url
        self.filepath = filepath
        self.progress_callback = progress_callback
        self.error_callback = error_callback
        self.cancel_event = cancel_event
        self.pause_event = pause_event
        self.num_threads = num_threads

    def run(self):
        """
        Starts the download in the background. Sends errors to the error function if they happen.
        """
        try:
            download_file(
                self.url,
                num_threads=self.num_threads,
                progress_callback=self.progress_callback,
                filepath=self.filepath,
                cancel_event=self.cancel_event,
                pause_event=self.pause_event
            )
        except Exception as e:
            self.error_callback(str(e))
