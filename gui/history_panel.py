"""
History Panel

Shows the list of past and current downloads.
Allows users to resume, view, open, or delete download items.
"""

import customtkinter as ctk
from gui.history_manager import load_history

class HistoryPanel(ctk.CTkFrame):
    """
    A frame that shows the download history table.
    """
    def __init__(self, master, app):
        """
        Initializes the HistoryPanel.

        Parameters:
            master (CTkFrame): The parent frame.
            app (CTk): The main application window.
        """
        super().__init__(master, fg_color="#181c24", corner_radius=0)
        self.app = app

        # Screen Title
        self.hist_title_label = ctk.CTkLabel(self, text="Downloads History", font=("Segoe UI Bold", 24), text_color="#b388ff")
        self.hist_title_label.place(relx=0.5, y=30, anchor="center")

        # Table Header Frame
        self.table_header = ctk.CTkFrame(self, fg_color="#1e232d", width=550, height=32, corner_radius=4)
        self.table_header.place(relx=0.5, y=70, x=-283, anchor="nw")

        # Table Headers
        ctk.CTkLabel(self.table_header, text="#", font=("Segoe UI Bold", 11), text_color="#aaa", width=25, anchor="w").place(x=5, y=5)
        ctk.CTkLabel(self.table_header, text="File Name", font=("Segoe UI Bold", 11), text_color="#aaa", width=150, anchor="w").place(x=35, y=5)
        ctk.CTkLabel(self.table_header, text="Size", font=("Segoe UI Bold", 11), text_color="#aaa", width=60, anchor="w").place(x=195, y=5)
        ctk.CTkLabel(self.table_header, text="Date Time", font=("Segoe UI Bold", 11), text_color="#aaa", width=110, anchor="w").place(x=265, y=5)
        ctk.CTkLabel(self.table_header, text="Status", font=("Segoe UI Bold", 11), text_color="#aaa", width=70, anchor="w").place(x=385, y=5)
        ctk.CTkLabel(self.table_header, text="Action", font=("Segoe UI Bold", 11), text_color="#aaa", width=80, anchor="w").place(x=465, y=5)

        # Scrollable list table
        self.scrollable_table = ctk.CTkScrollableFrame(self, fg_color="#181c24", width=570, height=380, corner_radius=0)
        self.scrollable_table.place(relx=0.5, y=110, x=-285, anchor="nw")

    def update_history_table(self):
        """
        Clears the table and reloads all downloads from the history file.
        """
        # Clear existing rows
        for widget in self.scrollable_table.winfo_children():
            widget.destroy()

        history = load_history()
        for idx, record in enumerate(history):
            row_frame = ctk.CTkFrame(self.scrollable_table, fg_color="#1c202a", height=42, corner_radius=6)
            row_frame.pack(fill="x", pady=4, padx=2)

            rec_id = record.get("id")

            # Index column
            ctk.CTkLabel(row_frame, text=str(idx + 1), font=("Segoe UI", 11), text_color="#aaa", width=25, anchor="w").place(x=5, y=8)
            
            # Filename column
            fname = record.get("filename", "")
            if len(fname) > 20:
                fname = fname[:17] + "..."
            ctk.CTkLabel(row_frame, text=fname, font=("Segoe UI Semibold", 11), text_color="#fff", width=150, anchor="w").place(x=35, y=8)
            
            # Size column
            ctk.CTkLabel(row_frame, text=record.get("size", "--"), font=("Segoe UI", 11), text_color="#aaa", width=60, anchor="w").place(x=195, y=8)
            
            # Date Time column
            ctk.CTkLabel(row_frame, text=record.get("datetime", "--"), font=("Segoe UI", 11), text_color="#aaa", width=110, anchor="w").place(x=265, y=8)
            
            # Status column
            status = record.get("status", "Unknown")
            status_colors = {
                "Completed": "#1abc9c",
                "Downloading": "green",
                "Paused": "orange",
                "Failed": "red",
                "Cancelled": "red"
            }
            ctk.CTkLabel(row_frame, text=status, font=("Segoe UI Bold", 11), text_color=status_colors.get(status, "#aaa"), width=70, anchor="w").place(x=385, y=8)
            
            # Action button configuration
            action_btn = None
            if status in ["Paused", "Cancelled", "Failed"]:
                action_btn = ctk.CTkButton(row_frame, text="Resume", width=50, height=24, font=("Segoe UI Bold", 10), fg_color="#7b2ff2", hover_color="#b388ff", command=lambda r=record: self.app.resume_download_record(r))
            elif status == "Downloading":
                if self.app.download_thread and self.app.download_thread.is_alive() and self.app.current_record_id == record.get("id"):
                    action_btn = ctk.CTkButton(row_frame, text="View", width=50, height=24, font=("Segoe UI Bold", 10), fg_color="#232946", hover_color="#7b2ff2", command=self.app.show_active_progress)
                else:
                    action_btn = ctk.CTkButton(row_frame, text="Resume", width=50, height=24, font=("Segoe UI Bold", 10), fg_color="#7b2ff2", hover_color="#b388ff", command=lambda r=record: self.app.resume_download_record(r))
            elif status == "Completed":
                action_btn = ctk.CTkButton(row_frame, text="Open", width=50, height=24, font=("Segoe UI Bold", 10), fg_color="#232946", hover_color="#7b2ff2", command=lambda r=record: self.app.open_downloaded_file(r))
            
            if action_btn:
                action_btn.place(x=465, y=8)

            # Inline Row Delete Button (x icon) next to Main Action Button
            delete_btn = ctk.CTkButton(row_frame, text="❌", width=22, height=24, font=("Segoe UI Bold", 10), fg_color="#e74c3c", hover_color="#c0392b", command=lambda rid=rec_id: self.app.delete_record_by_id(rid))
            delete_btn.place(x=525, y=8)
