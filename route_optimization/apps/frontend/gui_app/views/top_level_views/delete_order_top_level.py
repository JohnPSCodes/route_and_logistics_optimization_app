import tkinter as tk
from tkinter import ttk, messagebox
import requests
from route_optimization.config_user import JWT_TOKEN, API_URL_ORDERS
from apps.frontend.gui_app.utils.windows_utils import center_window

class DeleteOrderTopLevel(tk.Toplevel):
    def __init__(self, parent, order_data, callback):
        """
        order_data: dict with the fields of the order to delete
        callback: function to refresh the Treeview
        """
        super().__init__(parent)
        self.callback = callback
        self.order_id = order_data["id"]

        self.title(f"Delete Order {self.order_id}")
        self.geometry("350x200")
        self.resizable(False, False)
        center_window(self)

        # Confirmation message
        msg = f"Are you sure you want to delete Order {self.order_id}?\nCustomer: {order_data.get('customer_name')}"
        tk.Label(self, text=msg, wraplength=300, justify="center").pack(pady=30)

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Yes, Delete", command=self.submit).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancel", command=self.destroy).pack(side="left", padx=10)

    def submit(self):
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        try:
            response = requests.delete(f"{API_URL_ORDERS}{self.order_id}/", headers=headers, timeout=5)
            if response.status_code in (200, 204):
                messagebox.showinfo("Deleted", f"Order {self.order_id} has been deleted.")
                self.callback()  # refresh Treeview in parent frame
                self.destroy()
            else:
                messagebox.showerror("Error", f"Error deleting order: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", str(e))
