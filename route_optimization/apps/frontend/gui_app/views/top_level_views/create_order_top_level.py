# apps/frontend/gui_app/views/top_level_views/create_order.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import requests
from route_optimization.config_user import JWT_TOKEN, API_URL_ORDERS
from apps.frontend.gui_app.utils.windows_utils import center_window

class CreateOrderTopLevel(tk.Toplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        self.callback = callback
        self.title("Create Order")
        self.geometry("400x500")
        self.resizable(False, False)
        center_window(self)

        # ----------------- Campos del formulario -----------------
        self._build_form()

        # ----------------- Botón Crear -----------------
        ttk.Button(self, text="Create", command=self.submit).pack(pady=20)

    def _build_form(self):
        # Customer Name
        tk.Label(self, text="Customer Name").pack(anchor="w", padx=10)
        self.customer_entry = tk.Entry(self)
        self.customer_entry.pack(fill="x", padx=10, pady=5)

        # Address
        tk.Label(self, text="Address").pack(anchor="w", padx=10)
        self.address_entry = tk.Entry(self)
        self.address_entry.pack(fill="x", padx=10, pady=5)

        # Latitude
        tk.Label(self, text="Latitude").pack(anchor="w", padx=10)
        self.lat_entry = tk.Entry(self)
        self.lat_entry.pack(fill="x", padx=10, pady=5)

        # Longitude
        tk.Label(self, text="Longitude").pack(anchor="w", padx=10)
        self.lon_entry = tk.Entry(self)
        self.lon_entry.pack(fill="x", padx=10, pady=5)

        # Priority
        tk.Label(self, text="Priority").pack(anchor="w", padx=10)
        self.priority_spin = tk.Spinbox(self, from_=1, to=10)
        self.priority_spin.pack(fill="x", padx=10, pady=5)

        # Delivery Window Start
        tk.Label(self, text="Delivery Start").pack(anchor="w", padx=10)
        self.start_entry = DateEntry(self)
        self.start_entry.pack(fill="x", padx=10, pady=5)

        # Delivery Window End
        tk.Label(self, text="Delivery End").pack(anchor="w", padx=10)
        self.end_entry = DateEntry(self)
        self.end_entry.pack(fill="x", padx=10, pady=5)

        # Status
        tk.Label(self, text="Status").pack(anchor="w", padx=10)
        self.status_combo = ttk.Combobox(self, values=["pending", "assigned", "delivered"])
        self.status_combo.current(0)
        self.status_combo.pack(fill="x", padx=10, pady=5)

    def submit(self):
        # Validación mínima
        try:
            latitude = float(self.lat_entry.get())
            longitude = float(self.lon_entry.get())
            priority = int(self.priority_spin.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Latitude, Longitude must be numbers and Priority must be an integer.")
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
            response = requests.post(API_URL_ORDERS, json=data, headers=headers)
            if response.status_code == 201:
                self.callback()  # refresca treeview del frame padre
                self.destroy()
            else:
                messagebox.showerror("Error", f"Error creating order: {response.status_code}")
        except requests.RequestException as e:
            messagebox.showerror("Request Error", str(e))
