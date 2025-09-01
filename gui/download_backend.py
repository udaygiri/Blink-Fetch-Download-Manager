import threading
from function.Downloads import download_file

class DownloadThread(threading.Thread):
    def __init__(self, url, progress_callback, error_callback):
        super().__init__()
        self.url = url
        self.progress_callback = progress_callback
        self.error_callback = error_callback
        self._stop_event = threading.Event()

    def run(self):
        try:
            # Patch download_file to accept a progress_callback
            download_file(self.url, progress_callback=self.progress_callback)
        except Exception as e:
            self.error_callback(str(e))

    def stop(self):
        self._stop_event.set()

