import tkinter as tk
from tkinter import ttk, messagebox
from apps.backend.models import Route, Driver
from apps.backend.services.routes import assign_route

class AssignRouteTopLevel(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Assign Route to Driver")
        self.geometry("400x250")

        # Rutas
        tk.Label(self, text="Select Route:").pack(pady=5)
        self.route_cb = ttk.Combobox(self, state="readonly")
        self.route_cb.pack(pady=5)

        # Drivers
        tk.Label(self, text="Select Driver:").pack(pady=5)
        self.driver_cb = ttk.Combobox(self, state="readonly")
        self.driver_cb.pack(pady=5)

        # Cargar datos
        self.load_routes()
        self.load_drivers()

        # Botón
        tk.Button(self, text="Assign", command=self.assign).pack(pady=15)

    def load_routes(self):
        routes = Route.objects.all()
        self.routes_map = {f"{r.name} ({r.planned_date})": r.id for r in routes}
        self.route_cb["values"] = list(self.routes_map.keys())

    def load_drivers(self):
        drivers = Driver.objects.all()
        self.drivers_map = {f"{d.user.name} ({d.user.email})": d.id for d in drivers}
        self.driver_cb["values"] = list(self.drivers_map.keys())

    def assign(self):
        route_name = self.route_cb.get()
        driver_name = self.driver_cb.get()

        if not route_name or not driver_name:
            messagebox.showwarning("Warning", "Please select both route and driver.")
            return

        route_id = self.routes_map[route_name]
        driver_id = self.drivers_map[driver_name]

        assign_route(route_id, driver_id)
        messagebox.showinfo("Success", f"Assigned {driver_name} to {route_name}")
        self.destroy()
