import threading
from function.Downloads import download_file


class DownloadThread(threading.Thread):
    def __init__(self, url, filepath, progress_callback, error_callback):
        super().__init__()
        self.url = url
        self.filepath = filepath
        self.progress_callback = progress_callback
        self.error_callback = error_callback
        self._stop_event = threading.Event()

    def run(self):
        try:
            download_file(self.url, progress_callback=self.progress_callback, filepath=self.filepath)
        except Exception as e:
            self.error_callback(str(e))

    def stop(self):
        self._stop_event.set()

