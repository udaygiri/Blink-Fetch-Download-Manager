"""
Main GUI Window

Main window of the application. It creates and sets up the layout, sidebar,
and panels, and delegates settings and download tasks to their controllers.
"""

import os
import sys
import ctypes
import customtkinter as ctk
from tkinter import messagebox

from gui.sidebar import SidebarFrame
from gui.history_panel import HistoryPanel
from gui.add_download_panel import AddDownloadPanel
from gui.settings_panel import SettingsPanel
from gui.progress_panel import ProgressPanel
from gui.download_controller import DownloadController
from gui.settings_manager import load_settings, save_settings
from gui.history_manager import delete_download_record

class DownloadManagerApp(ctk.CTk):
    """
    The main download manager application window class.
    """
    def __init__(self):
        """
        Initializes the window size, theme, and child panels.
        """
        super().__init__()
        self.title("Blink Fetch Download Manager")
        self.geometry("800x520")
        self.resizable(True, True)
        self.minsize(800, 520)
        self.configure(fg_color="#181c24")

        # Set custom window and taskbar icon for Windows
        try:
            myappid = 'udaygiri.blinkfetch.downloadmanager.1.0'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

        icon_name = "Blink Fetch Download Manager logo.ico"
        icon_path = os.path.abspath(icon_name)
        if not os.path.exists(icon_path):
            dev_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            icon_path = os.path.join(dev_root, icon_name)
        if not os.path.exists(icon_path):
            base_path = getattr(sys, '_MEIPASS', None)
            if base_path:
                icon_path = os.path.join(base_path, icon_name)
        
        if os.path.exists(icon_path):
            try:
                self.iconbitmap(icon_path)
                # Overwrite CustomTkinter's default theme icon after the window maps
                self.after(200, lambda: self.iconbitmap(icon_path))
            except Exception:
                pass

        # Config variables
        # Locate user's system Downloads folder and use "Downloads/Blink Fetch"
        system_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
        self.default_download_path = os.path.join(system_downloads, "Blink Fetch")

        # Settings variables (Updated by SettingsPanel)
        self.settings_threads_var = ctk.StringVar(value="4")
        self.settings_theme_var = ctk.StringVar(value="Dark")

        # Load configuration preferences
        self.load_settings()

        # Instantiate core controller delegators
        self.controller = DownloadController(self)

        # ----------------------------------------------------
        # VIEW LAYER INITIALIZATION
        # ----------------------------------------------------
        # 1. Left Sidebar
        self.sidebar = SidebarFrame(self, on_switch_tab=self.switch_tab)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # 2. Main Content Container Frame (stretches dynamically)
        self.main_container = ctk.CTkFrame(self, fg_color="#181c24", corner_radius=0)
        self.main_container.pack(side="right", fill="both", expand=True)

        # 3. Instantiate Panels
        self.history_panel = HistoryPanel(self.main_container, self)
        self.add_panel = AddDownloadPanel(self.main_container, self)
        self.settings_panel = SettingsPanel(self.main_container, self)
        self.progress_panel = ProgressPanel(self.main_container, self)

        # Display history screen by default
        self.show_history_screen()

    # ----------------------------------------------------
    # CONTROLLER COMPATIBILITY PROPERTIES
    # ----------------------------------------------------
    @property
    def download_thread(self):
        """
        Returns the active download thread.
        """
        return self.controller.download_thread

    @property
    def current_record_id(self):
        """
        Returns the ID of the current download item.
        """
        return self.controller.current_record_id

    # ----------------------------------------------------
    # SETTINGS CONFIGURATION DELEGATORS
    # ----------------------------------------------------
    def save_settings(self, event=None):
        """
        Saves settings to the settings file.
        """
        if self.settings_threads_var is None or self.settings_theme_var is None:
            return
        save_settings(self.settings_threads_var.get(), self.settings_theme_var.get())

    def load_settings(self):
        """
        Loads settings from the settings file.
        """
        config = load_settings()
        if self.settings_threads_var is not None:
            self.settings_threads_var.set(config.get("threads", "4"))
        else:
            self.settings_threads_var = ctk.StringVar(value=config.get("threads", "4"))

        if self.settings_theme_var is not None:
            self.settings_theme_var.set(config.get("theme", "Dark"))
        else:
            self.settings_theme_var = ctk.StringVar(value=config.get("theme", "Dark"))

        ctk.set_appearance_mode(config.get("theme", "Dark"))

    def change_theme(self, choice):
        """
        Changes the theme color (Dark, Light, or System) and saves the setting.

        Parameters:
            choice (str): The theme name choice.
        """
        ctk.set_appearance_mode(choice)
        self.save_settings()

    # ----------------------------------------------------
    # ROUTING & SCREEN NAVIGATION MANAGEMENT
    # ----------------------------------------------------
    def hide_all_screens(self):
        """
        Hides all page panels.
        """
        self.history_panel.pack_forget()
        self.add_panel.pack_forget()
        self.settings_panel.pack_forget()
        self.progress_panel.pack_forget()

    def switch_tab(self, tab_name):
        """
        Switches the visible page panel when a sidebar tab is clicked.

        Parameters:
            tab_name (str): The name of the tab to load.
        """
        self.hide_all_screens()
        if tab_name == "history":
            self.history_panel.pack(fill="both", expand=True)
            self.history_panel.update_history_table()
        elif tab_name == "add":
            self.add_panel.pack(fill="both", expand=True)
        elif tab_name == "settings":
            self.settings_panel.pack(fill="both", expand=True)

    def show_history_screen(self):
        """
        Switches focus to the history screen.
        """
        self.sidebar.select_tab("history")

    def show_add_screen(self):
        """
        Switches focus to the add download screen.
        """
        self.sidebar.select_tab("add")

    def show_settings_screen(self):
        """
        Switches focus to the settings screen.
        """
        self.sidebar.select_tab("settings")

    def show_active_progress(self):
        """
        Shows the download progress panel.
        """
        self.hide_all_screens()
        self.progress_panel.pack(fill="both", expand=True)

    # ----------------------------------------------------
    # DOWNLOAD RUNTIME DELEGATORS
    # ----------------------------------------------------
    def start_download(self, url, folder, filename, size_str):
        """
        Starts a file download.

        Parameters:
            url (str): The link to download the file.
            folder (str): The folder to save it.
            filename (str): The name of the file.
            size_str (str): The file size string.
        """
        threads_count = int(self.settings_threads_var.get())
        self.controller.start_download(url, folder, filename, size_str, threads_count)

    def toggle_pause(self):
        """
        Pauses or resumes the current download.
        """
        self.controller.toggle_pause()

    def cancel_download(self):
        """
        Cancels the current download and deletes the local file.
        """
        filename = self.add_panel.filename_var.get().strip()
        folder = self.add_panel.folder_var.get().strip()
        self.controller.cancel_download(filename, folder)

    # ----------------------------------------------------
    # TABLE ACTIONS DELEGATORS
    # ----------------------------------------------------
    def delete_record_by_id(self, record_id):
        """
        Deletes a download record from the history.

        Parameters:
            record_id (str): The ID of the record.
        """
        if messagebox.askyesno("Delete Confirm", "Are you sure you want to delete this download record from history?"):
            delete_download_record(record_id)
            self.history_panel.update_history_table()

    def resume_download_record(self, record):
        """
        Resumes a paused, failed, or cancelled download record.

        Parameters:
            record (dict): The history record details.
        """
        threads_count = int(self.settings_threads_var.get())
        self.controller.resume_download_record(record, threads_count)

    def open_downloaded_file(self, record):
        """
        Opens the folder containing the downloaded file and highlights it.

        Parameters:
            record (dict): The history record details.
        """
        filepath = record.get("filepath")
        if filepath and os.path.exists(filepath):
            os.system(f'explorer /select,"{os.path.abspath(filepath)}"')
        else:
            messagebox.showerror("Error", "File does not exist or was deleted.")


if __name__ == "__main__":
    app = DownloadManagerApp()
    app.mainloop()
