"""
Sidebar Component

Renders the navigation menu on the left side of the application.
Communicates switching screen requests to the parent application.
"""

import customtkinter as ctk

class SidebarFrame(ctk.CTkFrame):
    """
    Left-hand sidebar navigation panel containing the logo and tab buttons.
    """
    def __init__(self, master, on_switch_tab):
        """
        Initializes the SidebarFrame.

        Parameters:
            master (CTk): The parent root application window.
            on_switch_tab (callable): Callback function invoked with the tab name ("history", "add", "settings").
        """
        super().__init__(master, fg_color="#13161c", width=180, corner_radius=0)
        self.on_switch_tab = on_switch_tab

        # Sidebar Title
        self.sidebar_title = ctk.CTkLabel(self, text="Blink Fetch", font=("Segoe UI Bold", 20), text_color="#b388ff")
        self.sidebar_title.place(relx=0.5, y=35, anchor="center")

        # Navigation Buttons
        self.nav_downloads_btn = ctk.CTkButton(self, text="Downloads", width=140, height=38, font=("Segoe UI Bold", 13), fg_color="#232946", hover_color="#7b2ff2", command=lambda: self.select_tab("history"), corner_radius=8)
        self.nav_downloads_btn.place(relx=0.5, y=100, anchor="center")

        self.nav_add_btn = ctk.CTkButton(self, text="+ Add Download", width=140, height=38, font=("Segoe UI Bold", 13), fg_color="#232946", hover_color="#7b2ff2", command=lambda: self.select_tab("add"), corner_radius=8)
        self.nav_add_btn.place(relx=0.5, y=150, anchor="center")

        self.nav_settings_btn = ctk.CTkButton(self, text="Settings", width=140, height=38, font=("Segoe UI Bold", 13), fg_color="#232946", hover_color="#7b2ff2", command=lambda: self.select_tab("settings"), corner_radius=8)
        self.nav_settings_btn.place(relx=0.5, y=200, anchor="center")

    def select_tab(self, tab_name):
        """
        Highlights the selected navigation button and triggers the switch tab callback.

        Parameters:
            tab_name (str): The name of the tab to select ("history", "add", "settings").
        """
        # Reset all button colors
        self.nav_downloads_btn.configure(fg_color="#232946")
        self.nav_add_btn.configure(fg_color="#232946")
        self.nav_settings_btn.configure(fg_color="#232946")

        # Highlight active button
        if tab_name == "history":
            self.nav_downloads_btn.configure(fg_color="#7b2ff2")
        elif tab_name == "add":
            self.nav_add_btn.configure(fg_color="#7b2ff2")
        elif tab_name == "settings":
            self.nav_settings_btn.configure(fg_color="#7b2ff2")

        # Trigger callback
        self.on_switch_tab(tab_name)
