"""
Add Download Panel Component

Manages the input interface for entering URLs, checking remote file details (names, sizes),
configuring save paths, and initiating a new download request.
"""

import os
import sys
import requests
import re
from email.header import decode_header
from tkinter import filedialog, messagebox
import customtkinter as ctk
from urllib.parse import urlparse
from function.File_path import sanitize_filename, get_category

# Category options with icons
CATEGORIES = [
    "🗜️ Compressed",
    "🖼️ Pictures",
    "🎬 Videos",
    "🎵 Music",
    "📄 Documents",
    "⚙️ Executables",
    "💻 Code",
    "📦 Others"
]

class AddDownloadPanel(ctk.CTkFrame):
    """
    Frame component containing URL entry, path selector, and start download buttons.
    """
    def __init__(self, master, app):
        """
        Initializes the AddDownloadPanel.

        Parameters:
            master (CTkFrame): The parent container frame.
            app (CTk): The main application window instance.
        """
        super().__init__(master, fg_color="#181c24", corner_radius=0)
        self.app = app

        # Title
        self.title_label = ctk.CTkLabel(self, text="Add Download", font=("Segoe UI Bold", 24), text_color="#b388ff")
        self.title_label.place(relx=0.5, y=40, anchor="center")

        # URL Input
        self.url_entry = ctk.CTkEntry(self, width=480, height=36, font=("Segoe UI", 13), corner_radius=10, placeholder_text="Paste download URL here...")
        self.url_entry.place(relx=0.5, y=95, anchor="center")

        # Category check box & Combo
        self.use_category_var = ctk.BooleanVar(value=True)
        self.use_category_cb = ctk.CTkCheckBox(self, text="Use Category", variable=self.use_category_var, font=("Segoe UI", 12), command=self.update_folder)
        self.use_category_cb.place(x=70, y=145, anchor="w")

        self.category_var = ctk.StringVar(value=CATEGORIES[0])
        self.category_combo = ctk.CTkComboBox(self, values=CATEGORIES, variable=self.category_var, width=160, font=("Segoe UI", 12), corner_radius=8, command=self.update_folder)
        self.category_combo.place(x=190, y=145, anchor="w")

        self.size_label = ctk.CTkLabel(self, text="File Size: --", text_color="#aaa", font=("Segoe UI", 12))
        self.size_label.place(x=370, y=145, anchor="w")

        # Save location selector
        self.folder_label = ctk.CTkLabel(self, text="Save to:", font=("Segoe UI", 12))
        self.folder_label.place(x=70, y=200, anchor="w")
        
        self.folder_var = ctk.StringVar(value=self.app.default_download_path)
        self.folder_entry = ctk.CTkEntry(self, width=270, height=32, textvariable=self.folder_var, font=("Segoe UI", 12), corner_radius=8)
        self.folder_entry.place(x=140, y=200, anchor="w")
        
        self.browse_btn = ctk.CTkButton(self, text="Browse", width=60, height=32, font=("Segoe UI", 11), fg_color="#232946", hover_color="#7b2ff2", command=self.browse_folder, corner_radius=8)
        self.browse_btn.place(x=420, y=200, anchor="w")

        # File name setting
        self.filename_label = ctk.CTkLabel(self, text="Filename:", font=("Segoe UI", 12))
        self.filename_label.place(x=70, y=250, anchor="w")
        
        self.filename_var = ctk.StringVar(value="")
        self.filename_entry = ctk.CTkEntry(self, width=340, height=32, textvariable=self.filename_var, font=("Segoe UI", 12), corner_radius=8)
        self.filename_entry.place(x=140, y=250, anchor="w")

        # Download trigger button
        self.download_btn = ctk.CTkButton(self, text="Download", width=160, height=40, font=("Segoe UI Bold", 14), fg_color="#7b2ff2", hover_color="#b388ff", command=self.trigger_download, corner_radius=10)
        self.download_btn.place(relx=0.5, y=325, anchor="center")

        # Bindings
        self.url_entry.bind('<FocusOut>', self.update_file_info)

    def browse_folder(self):
        """
        Opens a directory dialog picker and sets the selected folder path.
        """
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            self.app.default_download_path = folder

    def update_folder(self, event=None):
        """
        Updates the target folder path based on whether category mapping is checked.
        """
        if self.use_category_var.get():
            category = self.category_var.get()[2:]
            new_path = os.path.join(self.app.default_download_path, category)
            self.folder_var.set(os.path.abspath(new_path))

    def update_file_info(self, event=None):
        """
        Gets file info from the URL (name, size, type) when the user clicks out of the input box.
        """
        url = self.url_entry.get().strip()
        if not url:
            return
        try:
            # Get and sanitize filename
            response = requests.head(url, allow_redirects=True)
            if response.status_code != 200:
                response = requests.get(url, stream=True, allow_redirects=True)
            content_disposition = response.headers.get('Content-Disposition')
            filename = None
            if content_disposition:
                fname_match = re.search(r"filename\*?=(?:UTF-8''|\"|')?([^;\"']+)", content_disposition, re.IGNORECASE)
                if fname_match:
                    filename = fname_match.group(1)
                    if filename.startswith('=?') and filename.endswith('?='):
                        decoded_parts = decode_header(filename)
                        filename = ''.join([
                            part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
                            for part, encoding in decoded_parts
                        ])
            if not filename:
                filename = url.split("/")[-1]
            
            filename = sanitize_filename(filename)
            self.filename_var.set(filename)

            # File size
            size = int(response.headers.get('content-length', 0))
            size_str = f"{size/1e6:.2f} MB" if size else "--"
            self.size_label.configure(text=f"File Size: {size_str}")

            # Category mapping
            category = get_category(filename)
            cat_map = {
                "Compressed": "🗜️ Compressed",
                "Pictures": "🖼️ Pictures",
                "Videos": "🎬 Videos",
                "Music": "🎵 Music",
                "Documents": "📄 Documents",
                "Executables": "⚙️ Executables",
                "Code": "💻 Code",
                "Others": "📦 Others"
            }
            self.category_var.set(cat_map.get(category, "📦 Others"))
            self.update_folder()
        except Exception:
            self.size_label.configure(text="File Size: --")
            # Offline Fallback: Extract the filename, category, and path from the URL string itself
            try:
                from urllib.parse import urlparse
                path = urlparse(url).path
                filename = os.path.basename(path)
                if not filename:
                    filename = "downloaded_file"
                filename = sanitize_filename(filename)
                self.filename_var.set(filename)
                
                # Resolve category offline
                category = get_category(filename)
                cat_map = {
                    "Compressed": "🗜️ Compressed",
                    "Pictures": "🖼️ Pictures",
                    "Videos": "🎬 Videos",
                    "Music": "🎵 Music",
                    "Documents": "📄 Documents",
                    "Executables": "⚙️ Executables",
                    "Code": "💻 Code",
                    "Others": "📦 Others"
                }
                self.category_var.set(cat_map.get(category, "📦 Others"))
                self.update_folder()
            except Exception:
                self.filename_var.set("")


    def trigger_download(self):
        """
        Validates URL and initiates the active download process on the root application.
        """
        url = self.url_entry.get().strip()
        folder = self.folder_var.get().strip()
        filename = self.filename_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a download URL.")
            return

        size_str = self.size_label.cget('text').replace('File Size: ', '')
        self.app.start_download(url, folder, filename, size_str)
