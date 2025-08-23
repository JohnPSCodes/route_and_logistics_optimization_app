import tkinter as tk
from tkinter import ttk, messagebox
from apps.frontend.resources.google_maps import get_static_map
from route_optimization.config_user import GOOGLE_API_KEY
from apps.frontend.gui_app.views.top_level_views.add_way_point_top_level import AddWaypointTopLevel
from apps.backend.services.stops import get_route_stops
from apps.backend.services.routes import get_all_route
import webbrowser

class RoutesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        self.current_route_id = None

        # ---------- Grid config ----------
        self.grid_rowconfigure(2, weight=3)  # Mapa crece
        self.grid_rowconfigure(3, weight=1)  # Treeview crece
        self.grid_rowconfigure(4, weight=0)  # Botones fijos
        self.grid_columnconfigure(0, weight=1)

        # ---------- Top label ----------
        tk.Label(self, text="Routes", font=("Arial", 18), bg="white").grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # ---------- Route selection Combobox ----------
        frame_route = tk.Frame(self, bg="white")
        frame_route.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        frame_route.grid_columnconfigure(1, weight=1)

        ttk.Label(frame_route, text="Select Route:").grid(row=0, column=0, sticky="w")
        self.routes = get_all_route()
        self.route_map = {f"{r.name} ({r.planned_date})": r.id for r in self.routes}
        self.route_var = tk.StringVar()
        self.combobox_routes = ttk.Combobox(frame_route, values=list(self.route_map.keys()), textvariable=self.route_var)
        self.combobox_routes.grid(row=0, column=1, sticky="ew", padx=5)
        if self.routes:
            self.combobox_routes.current(0)
        self.combobox_routes.bind("<<ComboboxSelected>>", self.on_route_selected)

        # ---------- Map container ----------
        self.map_container = tk.Frame(self, bg="lightgray")
        self.map_container.grid(row=2, column=0, sticky="nsew", padx=20, pady=5)
        self.map_container.grid_rowconfigure(0, weight=1)
        self.map_container.grid_columnconfigure(0, weight=1)

        self.map_canvas = tk.Canvas(self.map_container, bg="lightblue")
        self.map_canvas.grid(row=0, column=0, sticky="nsew")
        self.map_canvas.bind("<Configure>", lambda e: self.load_map())

        # ---------- Stops Treeview ----------
        self.stops_tree = ttk.Treeview(self, columns=("stop_order","customer","lat","lng","eta","delivered"), show="headings", height=6)
        self.stops_tree.grid(row=3, column=0, sticky="nsew", padx=20, pady=5)
        for col, text, width in [
            ("stop_order","Stop #",50),
            ("customer","Customer",150),
            ("lat","Lat",80),
            ("lng","Lng",80),
            ("eta","ETA",120),
            ("delivered","Delivered",70)
        ]:
            self.stops_tree.heading(col, text=text)
            self.stops_tree.column(col, width=width, anchor="center" if col in ["stop_order","delivered"] else "w")

        # ---------- Buttons container ----------
        buttons_container = tk.Frame(self, bg="white")
        buttons_container.grid(row=4, column=0, sticky="ew", padx=10, pady=10)
        buttons_container.grid_columnconfigure((0,1,2), weight=1)

        ttk.Button(buttons_container, text="Add waypoint(stop)", command=self.add_waypoint).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Delete waypoint(stop)", command=self.delete_waypoint).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Load route", command=self.load_route).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="See all routes", command=self.see_all_routes).grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Open MAP (eliminate)", command=self.load_map).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Assign route", command=self.assign_route).grid(row=1, column=2, padx=5, pady=5, sticky="ew")

        # Cargar primer route si existe
        if self.routes:
            self.current_route_id = self.route_map[list(self.route_map.keys())[0]]
            self.refresh_all()

    # ---------- Route selection ----------
    def on_route_selected(self, event):
        route_name = self.route_var.get()
        if route_name in self.route_map:
            self.current_route_id = self.route_map[route_name]
            self.refresh_all()

    # ---------- Map handling ----------
    def load_map(self):
        if self.current_route_id is None:
            return
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()

        stops = get_route_stops(self.current_route_id)
        markers = [(s.order.latitude, s.order.longitude) for s in stops] if stops else [(18.61278955260962, -68.71589989505831)]
        center = f"{markers[0][0]},{markers[0][1]}" if markers else markers[0]
        path = "|".join([f"{s.order.latitude},{s.order.longitude}" for s in stops]) if stops else None

        self.map_img_tk = get_static_map(center=center, zoom=12, size=(width,height), markers=markers, path=path, api_key=GOOGLE_API_KEY, scale=1)
        if self.map_img_tk:
            self.map_canvas.delete("all")
            self.map_canvas.create_image(0,0, anchor="nw", image=self.map_img_tk)

    # ---------- Stops Treeview ----------
    def refresh_stops_list(self):
        for row in self.stops_tree.get_children():
            self.stops_tree.delete(row)
        if self.current_route_id is None:
            return
        stops = get_route_stops(self.current_route_id)
        for s in stops:
            self.stops_tree.insert("", "end", values=(
                s.stop_order,
                s.order.customer_name,
                s.order.latitude,
                s.order.longitude,
                s.estimated_arrival.strftime("%Y-%m-%d %H:%M"),
                "Yes" if s.delivered else "No"
            ))

    # ---------- Refresh everything ----------
    def refresh_all(self):
        self.load_map()
        self.refresh_stops_list()

    # ---------- Button actions ----------
    def add_waypoint(self):
        if self.current_route_id is None:
            messagebox.showwarning("Warning", "Please select a route first.")
            return
        AddWaypointTopLevel(self, route_id=self.current_route_id, refresh_callback=self.refresh_all)

    def delete_waypoint(self):
        messagebox.showinfo("Info", "Delete waypoint not implemented yet.")

    def load_route(self):
        """Abre Google Maps con todos los stops de la ruta seleccionada"""
        if self.current_route_id is None:
            messagebox.showwarning("Warning", "Please select a route first.")
            return

        stops = get_route_stops(self.current_route_id)
        if not stops:
            messagebox.showinfo("Info", "No stops for this route.")
            return

        coords_list = [f"{float(s.order.latitude)},{float(s.order.longitude)}" for s in stops]
        if len(coords_list) == 1:
            url = f"https://www.google.com/maps/search/?api=1&query={coords_list[0]}"
        else:
            url = "https://www.google.com/maps/dir/" + "/".join(coords_list)

        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir Google Maps: {e}")

    def see_all_routes(self):
        messagebox.showinfo("Info", "See all routes not implemented yet.")

    def assign_route(self):
        messagebox.showinfo("Info", "Assign route not implemented yet.")
