"""
Settings Panel Component

Renders the options panel allowing users to configure settings like thread count
and light/dark theme modes. Settings changes are persisted automatically.
"""

import customtkinter as ctk

class SettingsPanel(ctk.CTkFrame):
    """
    Frame component rendering the user preference settings interface.
    """
    def __init__(self, master, app):
        """
        Initializes the SettingsPanel.

        Parameters:
            master (CTkFrame): The parent container frame.
            app (CTk): The main application window instance to communicate settings changes.
        """
        super().__init__(master, fg_color="#181c24", corner_radius=0)
        self.app = app

        # Title
        self.settings_title_label = ctk.CTkLabel(self, text="Settings", font=("Segoe UI Bold", 24), text_color="#b388ff")
        self.settings_title_label.place(relx=0.5, y=40, anchor="center")

        # Thread Count Option
        ctk.CTkLabel(self, text="Threads Count:", font=("Segoe UI", 13), text_color="#fff").place(x=70, y=110, anchor="w")
        self.settings_threads_combo = ctk.CTkComboBox(self, values=["2", "4", "8", "12", "16"], variable=self.app.settings_threads_var, width=100, command=self.app.save_settings)
        self.settings_threads_combo.place(x=200, y=110, anchor="w")

        # Theme Option
        ctk.CTkLabel(self, text="Theme Mode:", font=("Segoe UI", 13), text_color="#fff").place(x=70, y=160, anchor="w")
        self.settings_theme_combo = ctk.CTkComboBox(self, values=["System", "Dark", "Light"], variable=self.app.settings_theme_var, width=100, command=self.app.change_theme)
        self.settings_theme_combo.place(x=200, y=160, anchor="w")
