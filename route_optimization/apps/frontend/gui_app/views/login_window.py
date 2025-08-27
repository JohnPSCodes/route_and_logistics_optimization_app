import tkinter as tk
from tkinter import ttk, messagebox
import requests
from apps.frontend.gui_app.utils.windows_utils import center_window
from route_optimization.config_user import LOGIN_URL, JWT_TOKEN
from apps.frontend.main import MainApp

API_LOGIN_URL = LOGIN_URL  # Adjust to your Django authentication endpoint

class LoginWindow(tk.Tk):
    """
    LoginWindow represents the login interface for the Route and Logistics application.
    It allows the user to authenticate with username and password.
    """

    def __init__(self):
        """
        Initialize the login window, configure styles, and create the UI components.
        """
        super().__init__()
        self.title("Login - Route and Logistics")
        self.geometry("300x300")
        center_window(self)  # Utility function to center the window on the screen
        self.config(bg="#f0f0f0")

        # 🎨 Configure ttk styles for a modern look
        style = ttk.Style(self)

        # Force a safe theme (important: some themes hide button text)
        style.theme_use("clam")

        style.configure("TFrame", background="#f0f0f0")
        style.configure("TLabel", background="#f0f0f0", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=6)

        # Main container frame
        frame = ttk.Frame(self, padding=30, style="TFrame")
        frame.pack(expand=True, fill="both")

        # Title label
        title = ttk.Label(
            frame,
            text="🔑 Login",
            font=("Segoe UI", 16, "bold"),
            anchor="center"
        )
        title.pack(pady=(0, 20))

        # Username field
        ttk.Label(frame, text="Username:").pack(anchor="w")
        self.username_var = tk.StringVar()
        self.entry_username = ttk.Entry(frame, textvariable=self.username_var, font=("Segoe UI", 11))
        self.entry_username.pack(fill="x", pady=5)

        # Password field
        ttk.Label(frame, text="Password:").pack(anchor="w")
        self.password_var = tk.StringVar()
        self.entry_password = ttk.Entry(frame, textvariable=self.password_var, show="*", font=("Segoe UI", 11))
        self.entry_password.pack(fill="x", pady=5)

        # Buttons container
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20, fill="x")

        # Login and Exit buttons
        tk.Button(btn_frame, text="🗝️ Login", command=self.login).pack(side="left", expand=True, fill="x", padx=5)
        tk.Button(btn_frame, text="❌ Exit", command=self.quit).pack(side="right", expand=True, fill="x", padx=5)

        # Bind Enter key to trigger login
        self.bind("<Return>", lambda e: self.login())

        # Focus on username input at startup
        self.entry_username.focus()

    def login(self):
        """
        Handle the login process:
        - Validate input fields.
        - Send authentication request to the API.
        - If successful, save the token and open the main application.
        """
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        # Input validation
        if not username or not password:
            messagebox.showwarning("Warning", "Please enter both username and password")
            return

        try:
            # API request to Django login endpoint
            response = requests.post(API_LOGIN_URL, data={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                token = data.get("access")  # JWT access token (if used)
                messagebox.showinfo("Success", f"Welcome {username}!")
                
                JWT_TOKEN = token

                # Save token for later use
                with open("auth_token.txt", "w") as f:
                    f.write(token)
                

                # Close login and launch main application
                self.destroy()
                app = MainApp()
                app.mainloop()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        except Exception as e:
            # Handle network or API errors
            messagebox.showerror("Error", f"Connection failed:\n{e}")


if __name__ == "__main__":
    login = LoginWindow()
    login.mainloop()
