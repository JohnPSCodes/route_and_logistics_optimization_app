
import tkinter as tk
from tkinter import ttk

class GeneralSettingsView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # Title
        ttk.Label(self, text="General Settings", font=("Arial", 14, "bold")).pack(pady=10)

        # Example setting: application name
        ttk.Label(self, text="Application Name:").pack(anchor="w", padx=20, pady=5)
        self.app_name_entry = ttk.Entry(self, width=40)
        self.app_name_entry.pack(padx=20)

        # Example setting: default timeout
        ttk.Label(self, text="Default Timeout (seconds):").pack(anchor="w", padx=20, pady=5)
        self.timeout_entry = ttk.Entry(self, width=10)
        self.timeout_entry.pack(padx=20)

        # Example setting: enable notifications
        self.notifications_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Enable Notifications", variable=self.notifications_var).pack(anchor="w", padx=20, pady=10)

        # Save button
        ttk.Button(self, text="Save", command=self.save_general_settings).pack(pady=15)

    def save_general_settings(self): ##### WORK ON ######
        app_name = self.app_name_entry.get()
        timeout = self.timeout_entry.get()
        notifications = self.notifications_var.get()
        # Placeholder for saving logic
        print(f"Saved General Settings: AppName={app_name}, Timeout={timeout}, Notifications={notifications}")