import tkinter as tk
from tkinter import ttk
from apps.frontend.gui_app.views.panels_views.api_settings import ApiSettingsView
from apps.frontend.gui_app.views.panels_views.user_preferences import UserPreferencesView
from apps.frontend.gui_app.views.panels_views.general_settings import GeneralSettingsView

class ConfigFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        # Title
        title = tk.Label(self, text="Configuration", font=("Arial", 18, "bold"), bg="white")
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # Configure grid for responsiveness
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # Left panel for navigation/options
        self.left_panel = tk.Frame(self, bg="#f5f5f5", relief="ridge", bd=1)
        self.left_panel.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.left_panel.grid_rowconfigure(0, weight=1)

        # Example options
        self.options_label = tk.Label(self.left_panel, text="Configuration Options", font=("Arial", 12, "bold"), bg="#f5f5f5")
        self.options_label.pack(anchor="nw", padx=10, pady=10)

        # Buttons
        ttk.Button(self.left_panel, text="General Settings",command=self.show_general_settings).pack(fill="x", padx=10, pady=5)
        ttk.Button(self.left_panel, text="API Settings",command=self.show_api_settings).pack(fill="x", padx=10, pady=5)
        ttk.Button(self.left_panel, text="User Preferences",command=self.show_user_preferences).pack(fill="x", padx=10, pady=5)

        # Right panel for settings detail
        self.right_panel = tk.Frame(self, bg="white", relief="ridge", bd=1)
        self.right_panel.grid(row=1, column=1, sticky="nsew", padx=20, pady=10)
        self.right_panel.grid_rowconfigure(0, weight=1)
        self.right_panel.grid_columnconfigure(0, weight=1)

        # Example: placeholder for dynamic settings content
        self.detail_placeholder = tk.Label(self.right_panel, text="Select an option to configure settings",
                                      bg="#f0f0f0", relief="groove")
        self.detail_placeholder.pack(fill="both", expand=True, padx=10, pady=10)

    def show_api_settings(self):
        """Replace right panel content with API settings view"""
        # Clear existing widgets
        self.clear_right_panel()

        # Load API settings view
        view = ApiSettingsView(self.right_panel)
        view.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_user_preferences(self):
        """Replace right panel content with User Preferences view"""
        self.clear_right_panel()
        view = UserPreferencesView(self.right_panel)
        view.pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_general_settings(self):
        """Replace right panel content with General Settings view"""
        self.clear_right_panel()
        view = GeneralSettingsView(self.right_panel)
        view.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_right_panel(self):
        """Utility to clear right panel before loading a new view"""
        for widget in self.right_panel.winfo_children():
            widget.destroy()
    
