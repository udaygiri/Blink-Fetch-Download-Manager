import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")


from gui.download_backend import DownloadThread

class DownloadManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Blink Fetch Download Manager")
        self.geometry("600x400")
        self.resizable(False, False)

        self.url_label = ctk.CTkLabel(self, text="Enter Download URL:")
        self.url_label.pack(pady=(30, 5))

        self.url_entry = ctk.CTkEntry(self, width=400, font=("Arial", 14))
        self.url_entry.pack(pady=5)

        self.download_btn = ctk.CTkButton(self, text="Start Download", command=self.start_download)
        self.download_btn.pack(pady=15)

        self.progress_label = ctk.CTkLabel(self, text="Progress:")
        self.progress_label.pack(pady=(20, 5))

        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="Idle", text_color="gray")
        self.status_label.pack(pady=10)

        self.download_thread = None

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a download URL.")
            return
        self.status_label.configure(text="Starting download...", text_color="blue")
        self.progress_bar.set(0)
        self.download_btn.configure(state="disabled")
        self.download_thread = DownloadThread(
            url,
            progress_callback=self.update_progress,
            error_callback=self.download_error
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
