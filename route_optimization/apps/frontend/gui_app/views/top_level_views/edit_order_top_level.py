
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import requests
from apps.frontend.gui_app.utils.windows_utils import center_window
from route_optimization.config_user import JWT_TOKEN, API_URL_ORDERS
from datetime import datetime


class EditOrderTopLevel(tk.Toplevel):
    def __init__(self, parent, order_data, callback):
        """
        order_data: dict with the fields of the order to edit
        callback: function to refresh Treeview
        """
        super().__init__(parent)
        self.callback = callback
        self.order_id = order_data["id"]

        self.title(f"Edit Order {self.order_id}")
        self.geometry("400x500")
        self.resizable(False, False)
        center_window(self)

        self._build_form(order_data)

        ttk.Button(self, text="Save Changes", command=self.submit).pack(pady=20)

    def _build_form(self, data):
        # Customer Name
        tk.Label(self, text="Customer Name").pack(anchor="w", padx=10)
        self.customer_entry = tk.Entry(self)
        self.customer_entry.insert(0, data.get("customer_name", ""))
        self.customer_entry.pack(fill="x", padx=10, pady=5)

        # Address
        tk.Label(self, text="Address").pack(anchor="w", padx=10)
        self.address_entry = tk.Entry(self)
        self.address_entry.insert(0, data.get("address", ""))
        self.address_entry.pack(fill="x", padx=10, pady=5)

        # Latitude
        tk.Label(self, text="Latitude").pack(anchor="w", padx=10)
        self.lat_entry = tk.Entry(self)
        self.lat_entry.insert(0, str(data.get("latitude", "")))
        self.lat_entry.pack(fill="x", padx=10, pady=5)

        # Longitude
        tk.Label(self, text="Longitude").pack(anchor="w", padx=10)
        self.lon_entry = tk.Entry(self)
        self.lon_entry.insert(0, str(data.get("longitude", "")))
        self.lon_entry.pack(fill="x", padx=10, pady=5)

        # Priority
        tk.Label(self, text="Priority").pack(anchor="w", padx=10)
        self.priority_spin = tk.Spinbox(self, from_=1, to=10)
        self.priority_spin.delete(0, "end")
        self.priority_spin.insert(0, str(data.get("priority", 1)))
        self.priority_spin.pack(fill="x", padx=10, pady=5)

        # Delivery Window Start
        tk.Label(self, text="Delivery Start").pack(anchor="w", padx=10)
        self.start_entry = DateEntry(self)
        start_str = data.get("delivery_window_start")[:10]  # 'YYYY-MM-DD'
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        self.start_entry.set_date(start_date)
        self.start_entry.pack(fill="x", padx=10, pady=5)

        # Delivery Window End
        tk.Label(self, text="Delivery End").pack(anchor="w", padx=10)
        self.end_entry = DateEntry(self)
        end_str = data.get("delivery_window_end")[:10]
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
        self.end_entry.set_date(end_date)
        self.end_entry.pack(fill="x", padx=10, pady=5)

        # Status
        tk.Label(self, text="Status").pack(anchor="w", padx=10)
        self.status_combo = ttk.Combobox(self, values=["pending", "assigned", "delivered"])
        self.status_combo.set(data.get("status", "pending"))
        self.status_combo.pack(fill="x", padx=10, pady=5)

    def submit(self):
        # Minimal validation
        try:
            latitude = float(self.lat_entry.get())
            longitude = float(self.lon_entry.get())
            priority = int(self.priority_spin.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Latitude and Longitude must be numbers, and Priority must be an integer.")
            return

        data = {
            "customer_name": self.customer_entry.get(),
            "address": self.address_entry.get(),
            "latitude": latitude,
            "longitude": longitude,
            "priority": priority,
            "delivery_window_start": self.start_entry.get_date().isoformat(),
            "delivery_window_end": self.end_entry.get_date().isoformat(),
            "status": self.status_combo.get()
        }

        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        try:
            response = requests.put(f"{API_URL_ORDERS}{self.order_id}/", json=data, headers=headers, timeout=5)
            if response.status_code in (200, 204):
                self.callback()  # refresh parent frame Treeview
                self.destroy()
            else:
                messagebox.showerror("Error", f"Error updating order: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", str(e))
