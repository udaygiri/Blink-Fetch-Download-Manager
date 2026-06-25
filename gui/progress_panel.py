"""
Progress Panel Component

Renders the download details and active progress for the current download session.
Provides real-time feedback on download speeds, percentage, and control buttons
to pause, resume, or cancel active tasks.
"""

import customtkinter as ctk

class ProgressPanel(ctk.CTkFrame):
    """
    Frame rendering progress bar, speed, size metrics, and pause/cancel buttons.
    """
    def __init__(self, master, app):
        """
        Initializes the ProgressPanel.

        Parameters:
            master (CTkFrame): The parent container frame.
            app (CTk): The main application window instance.
        """
        super().__init__(master, fg_color="#181c24", corner_radius=0)
        self.app = app

        # Screen Title
        self.prog_title_label = ctk.CTkLabel(self, text="Download Progress", font=("Segoe UI Bold", 24), text_color="#b388ff")
        self.prog_title_label.place(relx=0.5, y=30, anchor="center")

        # File Details
        self.filename_prog_label = ctk.CTkLabel(self, text="File Name: --", font=("Segoe UI Semibold", 20), text_color="#ffffff", justify="center", anchor="center", wraplength=480)
        self.filename_prog_label.place(relx=0.5, y=85, anchor="center")

        self.size_prog_label = ctk.CTkLabel(self, text="File Size: --", font=("Segoe UI", 16), text_color="#aaa", anchor="center")
        self.size_prog_label.place(relx=0.5, y=130, anchor="center")

        self.downloaded_prog_label = ctk.CTkLabel(self, text="Downloaded: --", font=("Segoe UI", 16), text_color="#aaa", anchor="center")
        self.downloaded_prog_label.place(relx=0.5, y=160, anchor="center")

        self.speed_prog_label = ctk.CTkLabel(self, text="Speed: --", font=("Segoe UI", 16), text_color="#aaa", anchor="center")
        self.speed_prog_label.place(relx=0.5, y=190, anchor="center")

        self.status_prog_label = ctk.CTkLabel(self, text="Status: Initializing...", font=("Segoe UI", 16), text_color="#aaa", anchor="center")
        self.status_prog_label.place(relx=0.5, y=220, anchor="center")

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self, width=480, height=12, progress_color="#7b2ff2", fg_color="#232946")
        self.progress_bar.set(0)
        self.progress_bar.place(relx=0.5, y=260, anchor="center")

        self.percentage_label = ctk.CTkLabel(self, text="0%", font=("Segoe UI Bold", 16), text_color="#b388ff")
        self.percentage_label.place(relx=0.5, y=285, anchor="center")

        # Control Buttons
        self.pause_btn = ctk.CTkButton(self, text="Pause", width=130, height=38, font=("Segoe UI Bold", 13), fg_color="#7b2ff2", hover_color="#b388ff", command=self.app.toggle_pause, corner_radius=10)
        self.pause_btn.place(relx=0.35, y=340, anchor="center")

        self.cancel_btn = ctk.CTkButton(self, text="Cancel", width=130, height=38, font=("Segoe UI Bold", 13), fg_color="#e74c3c", hover_color="#c0392b", command=self.app.cancel_download, corner_radius=10)
        self.cancel_btn.place(relx=0.65, y=340, anchor="center")

        self.back_btn = ctk.CTkButton(self, text="Back to Downloads", width=160, height=38, font=("Segoe UI Bold", 13), fg_color="#232946", hover_color="#7b2ff2", command=self.app.show_history_screen, corner_radius=10)
        self.back_btn.place(relx=0.5, y=400, anchor="center")

    def reset_ui(self, filename, size_str):
        """
        Resets and prepares the progress metrics interface for a new download task.

        Parameters:
            filename (str): The filename of the target file.
            size_str (str): The size string of the file (e.g. "45.2 MB").
        """
        self.filename_prog_label.configure(text=f"File Name: {filename}")
        self.size_prog_label.configure(text=f"File Size: {size_str}")
        self.downloaded_prog_label.configure(text="Downloaded: --")
        self.speed_prog_label.configure(text="Speed: --")
        self.status_prog_label.configure(text="Status: Starting download...", text_color="blue")
        self.progress_bar.set(0)
        self.percentage_label.configure(text="0%")
        self.pause_btn.configure(state="normal", text="Pause")
        self.cancel_btn.configure(state="normal")
        self.back_btn.configure(state="disabled", text="Back to Downloads")
