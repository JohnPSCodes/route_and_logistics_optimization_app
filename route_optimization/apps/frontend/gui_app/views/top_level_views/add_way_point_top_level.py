
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from apps.backend.services.stops import create_stop, get_route_stops
from apps.backend.services.orders import get_all_orders  # asumo que existe
from datetime import datetime
from apps.frontend.gui_app.utils.windows_utils import center_window


class AddWaypointTopLevel(tk.Toplevel):
    def __init__(self, parent, route_id=None, refresh_callback=None):
        super().__init__(parent)
        self.title("Add Waypoint")
        self.geometry("400x350")
        self.parent = parent
        self.route_id = route_id
        self.refresh_callback = refresh_callback
        center_window(self)

        # ---------Form------------
        ttk.Label(self, text="Select Order:").pack(pady=5, anchor="w")
        self.order_var = tk.StringVar()
        orders = get_all_orders()  # Lista de todos los orders
        self.order_map = {f"{o.customer_name} (ID:{o.id})": o.id for o in orders}
        self.combobox_order = ttk.Combobox(self, values=list(self.order_map.keys()), textvariable=self.order_var)
        self.combobox_order.pack(fill="x", padx=10)
        if orders:
            self.combobox_order.current(0)

        ttk.Label(self, text="Planned Arrival:").pack(pady=5, anchor="w")
        self.entry_date = DateEntry(self, date_pattern="yyyy-mm-dd")
        self.entry_date.pack(fill="x", padx=10)

        # ---------Buttons------------
        ttk.Button(self, text="Save", command=self.save_waypoint).pack(side="left", expand=True, padx=10, pady=10)
        ttk.Button(self, text="Cancel", command=self.destroy).pack(side="right", expand=True, padx=10, pady=10)

        


    def save_waypoint(self):
        try:
            order_name = self.order_var.get()
            if order_name not in self.order_map:
                messagebox.showwarning("Warning", "Please select a valid order")
                return

            order_id = self.order_map[order_name]

            # Calcular stop_order automáticamente
            existing_stops = get_route_stops(self.route_id)
            stop_order = len(existing_stops) + 1

            data = {
                "route_id": self.route_id,
                "order_id": order_id,
                "stop_order": stop_order,
                "estimated_arrival": datetime.combine(self.entry_date.get_date(), datetime.min.time()),
                "delivered": False
            }

            stop = create_stop(data)

            messagebox.showinfo("Success", f"Stop '{stop.order.customer_name}' added!")

            if self.refresh_callback:
                self.refresh_callback()

            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))