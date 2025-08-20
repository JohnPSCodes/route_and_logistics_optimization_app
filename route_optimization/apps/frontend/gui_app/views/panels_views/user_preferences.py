import tkinter as tk
from tkinter import ttk

class UserPreferencesView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        # Title
        ttk.Label(self, text="User Preferences", font=("Arial", 14, "bold")).pack(pady=10)

        # Example preference: theme selection
        ttk.Label(self, text="Theme:").pack(anchor="w", padx=20, pady=5)
        self.theme_var = tk.StringVar(value="Light")
        ttk.Combobox(self, textvariable=self.theme_var, values=["Light", "Dark"], state="readonly").pack(padx=20)

        # Example preference: language selection
        ttk.Label(self, text="Language:").pack(anchor="w", padx=20, pady=5)
        self.language_var = tk.StringVar(value="English")
        ttk.Combobox(self, textvariable=self.language_var,
                     values=["English", "Spanish", "French", "German"], state="readonly").pack(padx=20)

        # Save button
        ttk.Button(self, text="Save", command=self.save_preferences).pack(pady=15)

    def save_preferences(self): ##### WORK ON ######
        theme = self.theme_var.get()
        language = self.language_var.get()
        # Placeholder for saving logic (file, DB, settings, etc.)
        print(f"Saved preferences: Theme={theme}, Language={language}")