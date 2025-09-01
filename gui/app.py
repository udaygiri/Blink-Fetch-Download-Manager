import os
import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from gui.download_backend import DownloadThread

# Category options with icons (icon support is limited in customtkinter, so use text for now)
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




class DownloadManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Blink Fetch Download Manager")
        self.geometry("600x440")
        self.resizable(False, False)
        self.configure(fg_color="#181c24")

        # Default download path
        self.default_download_path = os.path.abspath("Downloads")

        # Title
        self.title_label = ctk.CTkLabel(self, text="Add Download", font=("Segoe UI Bold", 22), text_color="#b388ff")
        self.title_label.place(x=30, y=15)

        # URL
        self.url_entry = ctk.CTkEntry(self, width=440, height=36, font=("Segoe UI", 13), corner_radius=10, placeholder_text="Paste download URL here...")
        self.url_entry.place(x=30, y=55)

        # Category
        self.use_category_var = ctk.BooleanVar(value=True)
        self.use_category_cb = ctk.CTkCheckBox(self, text="Use Category", variable=self.use_category_var, font=("Segoe UI", 12), command=self.update_folder)
        self.use_category_cb.place(x=30, y=105)

        self.category_var = ctk.StringVar(value=CATEGORIES[0])
        self.category_combo = ctk.CTkComboBox(self, values=CATEGORIES, variable=self.category_var, width=170, font=("Segoe UI", 12), corner_radius=8, command=self.update_folder)
        self.category_combo.place(x=150, y=105)

        self.size_label = ctk.CTkLabel(self, text="File Size: --", text_color="#aaa", font=("Segoe UI", 12))
        self.size_label.place(x=350, y=105)

        # Folder
        self.folder_label = ctk.CTkLabel(self, text="Save to:", font=("Segoe UI", 12))
        self.folder_label.place(x=30, y=150)
        self.folder_var = ctk.StringVar(value=self.default_download_path)
        self.folder_entry = ctk.CTkEntry(self, width=320, height=32, textvariable=self.folder_var, font=("Segoe UI", 12), corner_radius=8)
        self.folder_entry.place(x=100, y=150)
        self.browse_btn = ctk.CTkButton(self, text="Browse", width=60, height=32, font=("Segoe UI", 11), fg_color="#232946", hover_color="#7b2ff2", command=self.browse_folder, corner_radius=8)
        self.browse_btn.place(x=430, y=150)

        # Filename
        self.filename_label = ctk.CTkLabel(self, text="Filename:", font=("Segoe UI", 12))
        self.filename_label.place(x=30, y=195)
        self.filename_var = ctk.StringVar(value="")
        self.filename_entry = ctk.CTkEntry(self, width=320, height=32, textvariable=self.filename_var, font=("Segoe UI", 12), corner_radius=8)
        self.filename_entry.place(x=100, y=195)

        # Download button
        self.download_btn = ctk.CTkButton(self, text="Download", width=120, height=38, font=("Segoe UI Bold", 14), fg_color="#7b2ff2", hover_color="#b388ff", command=self.start_download, corner_radius=10)
        self.download_btn.place(x=230, y=250)

        # Progress and status
        self.progress_label = ctk.CTkLabel(self, text="Progress:", font=("Segoe UI", 12))
        self.progress_label.place(x=30, y=320)

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.place(x=120, y=320)

        self.status_label = ctk.CTkLabel(self, text="Idle", text_color="gray", font=("Segoe UI", 12))
        self.status_label.place(x=30, y=360)

        self.download_thread = None
        self.current_url = None

        # Events
        self.url_entry.bind('<FocusOut>', self.update_file_info)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)
            self.default_download_path = folder

    def update_folder(self, event=None):
        if self.use_category_var.get():
            category = self.category_var.get()[2:]
            new_path = os.path.join(self.default_download_path, category)
            self.folder_var.set(os.path.abspath(new_path))

    def start_download(self):
        url = self.url_entry.get().strip()
        folder = self.folder_var.get().strip()
        filename = self.filename_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a download URL.")
            return
        self.status_label.configure(text="Starting download...", text_color="blue")
        self.progress_bar.set(0)
        self.download_btn.configure(state="disabled")
        # Save to folder/filename
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        self.current_url = url
        self.download_thread = DownloadThread(
            url,
            filepath,
            progress_callback=self.update_progress,
            error_callback=self.download_error
        )
        self.download_thread.start()

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def update_folder(self, event=None):
        if self.use_category_var.get():
            self.folder_var.set(os.path.abspath(f"Downloads/{self.category_var.get()[2:]}"))

    def update_file_info(self, event=None):
        url = self.url_entry.get().strip()
        if not url:
            return
        try:
            # Use file_path.py logic to get filename and category
            import importlib.util
            import sys
            spec = importlib.util.spec_from_file_location("file_path", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "function", "file_path.py")))
            file_path_mod = importlib.util.module_from_spec(spec)
            sys.modules["file_path"] = file_path_mod
            spec.loader.exec_module(file_path_mod)

            # Get filename using file_path.py logic (without creating folders)
            response = file_path_mod.requests.head(url, allow_redirects=True)
            if response.status_code != 200:
                response = file_path_mod.requests.get(url, stream=True, allow_redirects=True)
            content_disposition = response.headers.get('Content-Disposition')
            filename = None
            if content_disposition:
                fname_match = file_path_mod.re.search(r"filename\*?=(?:UTF-8''|\"|')?([^;\"']+)", content_disposition, file_path_mod.re.IGNORECASE)
                if fname_match:
                    filename = fname_match.group(1)
                    if filename.startswith('=?') and filename.endswith('?='):
                        decoded_parts = file_path_mod.decode_header(filename)
                        filename = ''.join([
                            part.decode(encoding or 'utf-8') if isinstance(part, bytes) else part
                            for part, encoding in decoded_parts
                        ])
            if not filename:
                filename = url.split("/")[-1]
            self.filename_var.set(filename)

            # File size
            size = int(response.headers.get('content-length', 0))
            size_str = f"{size/1e6:.2f} MB" if size else "--"
            self.size_label.configure(text=f"File Size: {size_str}")

            # Category
            category = file_path_mod.get_category(filename)
            # Map category to emoji label
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
            self.filename_var.set("")

    def start_download(self):
        url = self.url_entry.get().strip()
        folder = self.folder_var.get().strip()
        filename = self.filename_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a download URL.")
            return
        self.status_label.configure(text="Starting download...", text_color="blue")
        self.progress_bar.set(0)
        self.download_btn.configure(state="disabled")
        # Save to folder/filename
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, filename)
        self.current_url = url
        self.download_thread = DownloadThread(
            url,
            progress_callback=self.update_progress,
            error_callback=self.download_error,
            filepath=filepath
        )
        self.download_thread.start()

    def update_progress(self, downloaded, total):
        percent = downloaded / total if total else 0
        self.progress_bar.set(percent)
        self.status_label.configure(text=f"Downloading... {int(percent*100)}%", text_color="green")
        if percent >= 1.0:
            self.status_label.configure(text="Download Complete!", text_color="#1abc9c")
            self.download_btn.configure(state="normal")

    def download_error(self, error_msg):
        self.status_label.configure(text="Error!", text_color="red")
        self.download_btn.configure(state="normal")
        messagebox.showerror("Download Error", error_msg)

if __name__ == "__main__":
    app = DownloadManagerApp()
    app.mainloop()
