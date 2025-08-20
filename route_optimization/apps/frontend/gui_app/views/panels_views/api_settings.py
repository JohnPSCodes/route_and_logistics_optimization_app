
import tkinter as tk
from tkinter import ttk
from route_optimization.config_user import GOOGLE_API_KEY

class ApiSettingsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # Title
        ttk.Label(self, text="API Settings", font=("Arial", 14, "bold")).pack(pady=10)

        # API Key input
        ttk.Label(self, text="API Key:").pack(anchor="w", padx=20, pady=5)
        self.api_key_entry = ttk.Entry(self, width=40)
        self.api_key_entry.pack(padx=20)

        # Base URL input
        ttk.Label(self, text="Base URL:").pack(anchor="w", padx=20, pady=5)
        self.base_url_entry = ttk.Entry(self, width=40)
        self.base_url_entry.pack(padx=20)

        # Save button
        ttk.Button(self, text="Save", command=self.save_settings).pack(pady=15)

    def save_settings(self): ##### WORK ON #######
        api_key = self.api_key_entry.get()
        base_url = self.base_url_entry.get()
        # Placeholder for saving logic (file, DB, settings, etc.)
        print(f"Saved: API_KEY={api_key}, BASE_URL={base_url}")