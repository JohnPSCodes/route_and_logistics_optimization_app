import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from route_optimization.config_user import JWT_TOKEN, API_URL_USERS

class UserFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        # Title
        title = tk.Label(self, text="User / Client Management", font=("Arial", 18, "bold"), bg="white")
        title.grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # Configure main grid
        self.grid_rowconfigure(1, weight=1)  # row for user list
        self.grid_columnconfigure(0, weight=2)  # left panel
        self.grid_columnconfigure(1, weight=1)  # right panel

        # Left panel: Treeview of users
        left_panel = tk.Frame(self, bg="white")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)

        self.user_tree = ttk.Treeview(left_panel, columns=("user_id","name","email"), show="headings")
        self.user_tree.heading("user_id", text="ID")
        self.user_tree.heading("name", text="Name")
        self.user_tree.heading("email", text="Email")
        self.user_tree.grid(row=0, column=0, sticky="nsew")

        # Columns sizing
        self.user_tree.column("user_id", width=50, anchor="center")
        self.user_tree.column("name", width=175, anchor="center")
        self.user_tree.column("email", width=175, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Bind selection to populate right panel
        self.user_tree.bind("<<TreeviewSelect>>", self.on_user_select)

        # Right panel: user details and actions
        right_panel = tk.Frame(self, bg="#f0f0f0", relief="ridge", bd=1)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        tk.Label(right_panel, text="User Details", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)

        tk.Label(right_panel, text="Name:", bg="#f0f0f0").pack(anchor="w", padx=10, pady=2)
        self.name_entry = ttk.Entry(right_panel)
        self.name_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(right_panel, text="Email:", bg="#f0f0f0").pack(anchor="w", padx=10, pady=2)
        self.email_entry = ttk.Entry(right_panel)
        self.email_entry.pack(fill="x", padx=10, pady=2)

        tk.Label(right_panel, text="Password:", bg="#f0f0f0").pack(anchor="w", padx=10, pady=2)
        self.password_entry = ttk.Entry(right_panel, show="*")
        self.password_entry.pack(fill="x", padx=10, pady=2)

        # Action buttons
        button_frame = tk.Frame(right_panel, bg="#f0f0f0")
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add User", command=self.add_user).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update User", command=self.update_user).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete User", command=self.delete_user).grid(row=0, column=2, padx=5)

        # Load users on start
        self.load_users_from_api()

    def load_users_from_api(self):
        """Load all users from the API and populate the Treeview"""
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        try:
            response = requests.get(API_URL_USERS, headers=headers, timeout=5)
            if response.status_code == 200:
                users = response.json()

                # Clear the Treeview
                for iid in self.user_tree.get_children():
                    self.user_tree.delete(iid)

                # Insert users into the Treeview
                for user in users:
                    self.user_tree.insert(
                        "",
                        "end",
                        values=(
                            user.get("user_id"),
                            user.get("name"),
                            user.get("email"),
                        )
                    )
            else:
                print("Error loading users:", response.status_code, response.text)
        except requests.RequestException as e:
            print("Connection error while loading users:", e)

    def on_user_select(self, event):
        """Populate entry fields when a user is selected"""
        selected = self.user_tree.selection()
        if selected:
            user = self.user_tree.item(selected[0])["values"]
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, user[1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, user[2])
            self.password_entry.delete(0, tk.END)

    def add_user(self):
        """Add a new user via API"""
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        if not name or not email or not password:
            print("Please fill in all fields")
            return
        data = {"name": name, "email": email, "password_hash": password}
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        try:
            response = requests.post(API_URL_USERS, json=data, headers=headers)
            if response.status_code in (200, 201):
                print("User added successfully")
                self.load_users_from_api()
            else:
                print("Error adding user:", response.status_code, response.text)
        except requests.RequestException as e:
            print("Connection error while adding user:", e)

    def update_user(self):
        """Update the selected user via API"""
        selected = self.user_tree.selection()
        if not selected:
            print("Please select a user to update")
            return
        user_id = self.user_tree.item(selected[0])["values"][0]
        data = {
            "name": self.name_entry.get().strip(),
            "email": self.email_entry.get().strip()
        }
        if self.password_entry.get().strip():
            data["password_hash"] = self.password_entry.get().strip()
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        
        # Correct URL (avoid double slash)
        response = requests.put(f"{API_URL_USERS.rstrip('/')}/{user_id}/", json=data, headers=headers)
        if response.status_code == 200:
            print("User updated successfully")
            self.load_users_from_api()
        else:
            print("Error updating user:", response.status_code, response.text)

    
    def delete_user(self):
        """Delete the selected user via API with confirmation including user name"""
        selected = self.user_tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a user to delete")
            return

        user_item = self.user_tree.item(selected[0])
        user_id = user_item["values"][0]
        user_name = user_item["values"][1]  # assuming 'name' is the second column

        # Ask for confirmation including user name
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{user_name}' (ID {user_id})?")
        if not confirm:
            return  # User cancelled

        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        url = f"{API_URL_USERS.rstrip('/')}/{user_id}/"

        try:
            response = requests.delete(url, headers=headers)
            if response.status_code in (200, 204):
                messagebox.showinfo("Deleted", f"User '{user_name}' deleted successfully")
                self.load_users_from_api()
            else:
                messagebox.showerror("Error", f"Error deleting user '{user_name}': {response.status_code}\n{response.text}")
        except requests.RequestException as e:
            messagebox.showerror("Connection Error", f"Error connecting to server while deleting user '{user_name}': {e}")
