"""
Download Controller

Manages the download process, starts the background threads, and updates
the screen of the application.
"""

import os
import time
import threading
from tkinter import messagebox

from gui.download_backend import DownloadThread
from gui.history_manager import add_download_record, update_download_status
from gui.utils import format_speed, format_size

class DownloadController:
    """
    Handles downloading files, measuring speed, pausing or canceling, and
    updating the progress labels on the screen.
    """
    def __init__(self, app):
        """
        Initializes the DownloadController.

        Parameters:
            app (CTk): The main application window.
        """
        self.app = app
        self.download_thread = None
        self.current_record_id = None
        self.cancel_event = None
        self.pause_event = None
        self.start_time = 0
        self.last_update_time = 0
        self.last_downloaded_bytes = 0

    def start_download(self, url, folder, filename, size_str, num_threads):
        """
        Prepares the progress screen, saves a history record, and starts the download thread.

        Parameters:
            url (str): The web link of the file.
            folder (str): The folder where the file will be saved.
            filename (str): The name of the file.
            size_str (str): The size of the file as text.
            num_threads (int): How many threads to use for downloading.
        """
        self.app.progress_panel.reset_ui(filename, size_str)
        self.app.show_active_progress()

        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)

        self.cancel_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()

        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_downloaded_bytes = 0

        self.current_record_id = add_download_record(url, filename, filepath, size_str, 0)
        update_download_status(self.current_record_id, "Downloading")

        self.download_thread = DownloadThread(
            url,
            filepath,
            progress_callback=lambda downloaded, total: self.app.after(0, self.update_progress, downloaded, total),
            error_callback=lambda error_msg: self.app.after(0, self.download_error, error_msg),
            cancel_event=self.cancel_event,
            pause_event=self.pause_event,
            num_threads=num_threads
        )
        self.download_thread.start()

    def update_progress(self, downloaded, total):
        """
        Updates the progress bar, percentage, speed, and downloaded text on the screen.

        Parameters:
            downloaded (int): How many bytes have been downloaded so far.
            total (int): The total size of the file in bytes.
        """
        if self.cancel_event and self.cancel_event.is_set():
            return
        if self.pause_event and not self.pause_event.is_set():
            return

        percent = downloaded / total if total else 0
        self.app.progress_panel.progress_bar.set(percent)
        self.app.progress_panel.percentage_label.configure(text=f"{int(percent * 100)}%")

        total_str = format_size(total) if total else "--"
        self.app.progress_panel.downloaded_prog_label.configure(
            text=f"Downloaded: {format_size(downloaded)} / {total_str}"
        )

        now = time.time()
        elapsed = now - self.last_update_time
        if elapsed >= 0.5:
            bytes_diff = downloaded - self.last_downloaded_bytes
            speed = bytes_diff / elapsed
            self.app.progress_panel.speed_prog_label.configure(text=f"Speed: {format_speed(speed)}")
            self.last_update_time = now
            self.last_downloaded_bytes = downloaded

        self.app.progress_panel.status_prog_label.configure(text="Status: Downloading...", text_color="green")

        if percent >= 1.0:
            self.app.progress_panel.status_prog_label.configure(text="Status: Download Complete!", text_color="#1abc9c")
            self.app.progress_panel.speed_prog_label.configure(text="Speed: Completed")
            self.app.progress_panel.pause_btn.configure(state="disabled")
            self.app.progress_panel.cancel_btn.configure(state="disabled")
            self.app.progress_panel.back_btn.configure(state="normal", text="Back to Downloads")
            if self.current_record_id:
                update_download_status(self.current_record_id, "Completed", downloaded, total)

    def download_error(self, error_msg):
        """
        Shows an error message and updates the status if the download fails.

        Parameters:
            error_msg (str): The error message details.
        """
        if self.cancel_event and self.cancel_event.is_set():
            return
        self.app.progress_panel.status_prog_label.configure(text="Status: Error occurred!", text_color="red")
        self.app.progress_panel.speed_prog_label.configure(text="Speed: --")
        self.app.progress_panel.pause_btn.configure(state="disabled")
        self.app.progress_panel.cancel_btn.configure(state="disabled")
        self.app.progress_panel.back_btn.configure(state="normal", text="Back to Downloads")
        if self.current_record_id:
            update_download_status(self.current_record_id, "Failed")
        messagebox.showerror("Download Error", error_msg)

    def toggle_pause(self):
        """
        Pauses or resumes the download process.
        """
        if self.pause_event is not None:
            if self.pause_event.is_set():
                self.pause_event.clear()
                self.app.progress_panel.pause_btn.configure(text="Resume")
                self.app.progress_panel.status_prog_label.configure(text="Status: Paused", text_color="orange")
                self.app.progress_panel.speed_prog_label.configure(text="Speed: 0.00 B/s")
                if self.current_record_id:
                    update_download_status(self.current_record_id, "Paused")
            else:
                self.pause_event.set()
                self.app.progress_panel.pause_btn.configure(text="Pause")
                self.app.progress_panel.status_prog_label.configure(text="Status: Downloading...", text_color="green")
                if self.current_record_id:
                    update_download_status(self.current_record_id, "Downloading")
                self.last_update_time = time.time()

    def cancel_download(self, filename, folder):
        """
        Cancels the active download and deletes the partially downloaded file.

        Parameters:
            filename (str): The name of the file.
            folder (str): The folder containing the file.
        """
        if self.cancel_event is not None:
            self.cancel_event.set()
        if self.pause_event is not None:
            self.pause_event.set()

        self.app.progress_panel.status_prog_label.configure(text="Status: Cancelled", text_color="red")
        self.app.progress_panel.speed_prog_label.configure(text="Speed: --")
        self.app.progress_panel.pause_btn.configure(state="disabled")
        self.app.progress_panel.cancel_btn.configure(state="disabled")
        self.app.progress_panel.back_btn.configure(state="normal", text="Back to Downloads")
        if self.current_record_id:
            update_download_status(self.current_record_id, "Cancelled")

        filepath = os.path.join(folder, filename)

        def try_delete():
            time.sleep(0.3)
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
            except Exception:
                pass

        threading.Thread(target=try_delete, daemon=True).start()

    def resume_download_record(self, record, num_threads):
        """
        Resumes a paused, failed, or cancelled download record.

        Parameters:
            record (dict): The history record dictionary.
            num_threads (int): The number of threads to use.
        """
        url = record.get("url")
        filepath = record.get("filepath")
        filename = record.get("filename")
        size = record.get("size")

        self.app.progress_panel.reset_ui(filename, size)
        self.app.progress_panel.status_prog_label.configure(text="Status: Resuming...", text_color="blue")
        self.app.show_active_progress()

        self.cancel_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()

        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_downloaded_bytes = 0
        self.current_record_id = record.get("id")

        update_download_status(self.current_record_id, "Downloading")

        self.download_thread = DownloadThread(
            url,
            filepath,
            progress_callback=lambda downloaded, total: self.app.after(0, self.update_progress, downloaded, total),
            error_callback=lambda error_msg: self.app.after(0, self.download_error, error_msg),
            cancel_event=self.cancel_event,
            pause_event=self.pause_event,
            num_threads=num_threads
        )
        self.download_thread.start()
