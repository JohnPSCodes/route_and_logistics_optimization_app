# dashboard_frame.py
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser

# Integra con tus servicios existentes:
from apps.backend.services.routes import get_all_route
from apps.backend.services.stops import get_route_stops
from apps.backend.services.routes_info import get_full_route_info, get_route_driver
from apps.frontend.resources.google_maps import get_static_map
from route_optimization.config_user import GOOGLE_API_KEY


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller=None):
        super().__init__(parent, bg="white")
        self.controller = controller

        # --- State ---
        self.route_rows = {}   # Tree iid -> route_id
        self.map_img_tk = None

        # --- Layout grid ---
        self.grid_rowconfigure(2, weight=1)   # centro (tabla + detalle) crece
        self.grid_columnconfigure(0, weight=1)

        # --- Title ---
        ttk.Label(self, text="Dashboard", font=("Arial", 18)).grid(
            row=0, column=0, sticky="w", padx=12, pady=(10, 6)
        )

        # --- KPI cards (fila superior) ---
        kpis = tk.Frame(self, bg="white")
        kpis.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 8))
        for i in range(4):
            kpis.grid_columnconfigure(i, weight=1)

        self.kpi_vars = {
            "total_routes": tk.StringVar(value="0"),
            "planned": tk.StringVar(value="0"),
            "in_progress": tk.StringVar(value="0"),
            "completed": tk.StringVar(value="0"),
        }

        self._make_kpi(kpis, 0, "Total Routes", self.kpi_vars["total_routes"])
        self._make_kpi(kpis, 1, "Planned", self.kpi_vars["planned"])
        self._make_kpi(kpis, 2, "In Progress", self.kpi_vars["in_progress"])
        self._make_kpi(kpis, 3, "Completed", self.kpi_vars["completed"])

        # --- Centro: tabla + detalle ---
        center = tk.Frame(self, bg="white")
        center.grid(row=2, column=0, sticky="nsew", padx=12, pady=8)
        center.grid_columnconfigure(0, weight=3)
        center.grid_columnconfigure(1, weight=2)
        center.grid_rowconfigure(0, weight=1)

        # Tabla de rutas (izquierda)
        left = tk.Frame(center, bg="white")
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        left.grid_rowconfigure(1, weight=1)
        ttk.Label(left, text="Routes").grid(row=0, column=0, sticky="w", pady=(0, 6))

        cols = ("name", "date", "status", "driver", "stops", "done")
        self.routes_tv = ttk.Treeview(left, columns=cols, show="headings", height=12)
        for col, txt, w in [
            ("name", "Name", 160),
            ("date", "Date", 90),
            ("status", "Status", 100),
            ("driver", "Driver", 140),
            ("stops", "Stops", 60),
            ("done", "Completed", 80),
        ]:
            self.routes_tv.heading(col, text=txt)
            self.routes_tv.column(col, width=w, anchor="w")
        self.routes_tv.grid(row=1, column=0, sticky="nsew")

        yscroll = ttk.Scrollbar(left, orient="vertical", command=self.routes_tv.yview)
        self.routes_tv.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=1, column=1, sticky="ns")

        self.routes_tv.bind("<<TreeviewSelect>>", self.on_route_select)

        # Panel de detalle (derecha) con info + mini-mapa
        right = tk.Frame(center, bg="white", bd=1, relief="solid")
        right.grid(row=0, column=1, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(3, weight=1)

        ttk.Label(right, text="Route Detail", font=("Arial", 12, "bold")).grid(
            row=0, column=0, sticky="w", padx=10, pady=(8, 4)
        )

        info = tk.Frame(right, bg="white")
        info.grid(row=1, column=0, sticky="ew", padx=10)
        for i in range(2):
            info.grid_columnconfigure(i, weight=1)

        self.detail_vars = {
            "name": tk.StringVar(value="—"),
            "status": tk.StringVar(value="—"),
            "driver": tk.StringVar(value="—"),
            "stops": tk.StringVar(value="0"),
            "completed": tk.StringVar(value="0"),
            "distance": tk.StringVar(value="0 km"),
            "duration": tk.StringVar(value="00h 00m"),
        }

        self._row(info, 0, "Name:", self.detail_vars["name"])
        self._row(info, 1, "Status:", self.detail_vars["status"])
        self._row(info, 2, "Driver:", self.detail_vars["driver"])
        self._row(info, 3, "Stops:", self.detail_vars["stops"])
        self._row(info, 4, "Completed:", self.detail_vars["completed"])
        self._row(info, 5, "Distance:", self.detail_vars["distance"])
        self._row(info, 6, "Duration:", self.detail_vars["duration"])

        # Mini-mapa
        self.map_canvas = tk.Canvas(right, bg="#f2f2f2", height=220, highlightthickness=0)
        self.map_canvas.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.map_canvas.bind("<Configure>", lambda e: self._redraw_map())

        # Botones de acción rápida
        actions = tk.Frame(right, bg="white")
        actions.grid(row=4, column=0, sticky="ew", padx=10, pady=(0, 10))
        actions.grid_columnconfigure((0, 1), weight=1)
        ttk.Button(actions, text="Open in Maps", command=self._open_selected_in_maps).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(actions, text="Refresh", command=self.refresh_all).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

        # --- Inicial ---
        self.refresh_all()

    # ---------------- Helpers UI ----------------
    def _make_kpi(self, parent, col, title, var):
        card = tk.Frame(parent, bg="#ffffff", bd=1, relief="solid")
        card.grid(row=0, column=col, sticky="ew", padx=(0 if col == 0 else 8, 0))
        card.grid_columnconfigure(0, weight=1)
        ttk.Label(card, text=title, font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", padx=10, pady=(8, 0)
        )
        ttk.Label(card, textvariable=var, font=("Arial", 20, "bold")).grid(
            row=1, column=0, sticky="w", padx=10, pady=(0, 8)
        )

    def _row(self, parent, r, label, var):
        ttk.Label(parent, text=label).grid(row=r, column=0, sticky="w", pady=2)
        ttk.Label(parent, textvariable=var).grid(row=r, column=1, sticky="w", pady=2)

    # ---------------- Data refresh ----------------
    def refresh_all(self):
        """Recarga KPIs, tabla de rutas y limpia detalle/mapa si no hay selección."""
        try:
            routes = get_all_route()
        except Exception as e:
            messagebox.showerror("Error", f"Cannot load routes: {e}")
            routes = []

        # KPIs
        total = len(routes)
        planned = sum(1 for r in routes if getattr(r, "status", "") == "planned")
        in_progress = sum(1 for r in routes if getattr(r, "status", "") == "in_progress")
        completed = sum(1 for r in routes if getattr(r, "status", "") == "completed")

        self.kpi_vars["total_routes"].set(str(total))
        self.kpi_vars["planned"].set(str(planned))
        self.kpi_vars["in_progress"].set(str(in_progress))
        self.kpi_vars["completed"].set(str(completed))

        # Tabla
        for iid in self.routes_tv.get_children():
            self.routes_tv.delete(iid)
        self.route_rows.clear()

        for r in routes:
            # Driver (rápido, sin API de distancia)
            try:
                driver_name = get_route_driver(r.id) or "Unassigned"
            except Exception:
                driver_name = "Unassigned"

            # Stops
            try:
                stops = get_route_stops(r.id)
                total_stops = len(stops)
                completed_stops = sum(1 for s in stops if getattr(s, "delivered", False))
            except Exception:
                total_stops, completed_stops = 0, 0

            values = (
                getattr(r, "name", "—"),
                str(getattr(r, "planned_date", "")),
                getattr(r, "status", "—"),
                driver_name,
                str(total_stops),
                str(completed_stops),
            )
            iid = self.routes_tv.insert("", "end", values=values)
            self.route_rows[iid] = r.id

        # Limpia detalle si no hay selección
        if not self.routes_tv.selection():
            self._clear_detail()

    def _clear_detail(self):
        for key in self.detail_vars:
            self.detail_vars[key].set("—" if key not in ("stops", "completed") else "0")
        self._clear_map()

    # ---------------- Selection handlers ----------------
    def on_route_select(self, _event=None):
        sel = self.routes_tv.selection()
        if not sel:
            self._clear_detail()
            return
        iid = sel[0]
        route_id = self.route_rows.get(iid)
        if not route_id:
            self._clear_detail()
            return

        # Info detallada (usa Distance Matrix dentro de get_full_route_info)
        try:
            info = get_full_route_info(route_id)
        except Exception as e:
            messagebox.showwarning("Warning", f"Cannot load route info: {e}")
            self._clear_detail()
            return

        # Actualiza labels
        vals = self.routes_tv.item(iid, "values")
        self.detail_vars["name"].set(vals[0] if vals else "—")
        self.detail_vars["status"].set(vals[2] if len(vals) > 2 else "—")
        self.detail_vars["driver"].set(info.get("driver", "Unassigned") or "Unassigned")
        self.detail_vars["stops"].set(str(info.get("total_stops", 0)))
        self.detail_vars["completed"].set(str(info.get("completed_stops", 0)))
        self.detail_vars["distance"].set(f"{info.get('distance_km', 0)} km")
        # duration puede venir como "00h 00m" si lo implementaste así
        dur_str = info.get("duration") or f"{info.get('duration_min', 0)} min"
        self.detail_vars["duration"].set(dur_str)

        # Mini-mapa
        self._draw_map_for_route(route_id)

    # ---------------- Mini-map ----------------
    def _clear_map(self):
        self.map_canvas.delete("all")
        self.map_img_tk = None

    def _redraw_map(self):
        # Re-dibuja el mapa si hay selección
        sel = self.routes_tv.selection()
        if sel:
            route_id = self.route_rows.get(sel[0])
            if route_id:
                self._draw_map_for_route(route_id)

    def _draw_map_for_route(self, route_id):
        # Obtiene paradas y pinta un static map en el canvas derecho
        try:
            stops = get_route_stops(route_id)
        except Exception:
            stops = []

        width = max(self.map_canvas.winfo_width(), 300)
        height = max(self.map_canvas.winfo_height(), 200)

        if not stops:
            self._clear_map()
            self.map_canvas.create_text(
                width // 2,
                height // 2,
                text="No stops",
                anchor="center",
                font=("Arial", 12),
            )
            return

        markers = [(s.order.latitude, s.order.longitude) for s in stops]
        center = f"{markers[0][0]},{markers[0][1]}"
        path = "|".join([f"{lat},{lng}" for (lat, lng) in markers])

        try:
            self.map_img_tk = get_static_map(
                center=center,
                zoom=12,
                size=(width, height),
                markers=markers,
                path=path,
                api_key=GOOGLE_API_KEY,
                scale=1,
            )
        except Exception:
            self.map_img_tk = None

        self.map_canvas.delete("all")
        if self.map_img_tk:
            self.map_canvas.create_image(0, 0, anchor="nw", image=self.map_img_tk)
        else:
            self.map_canvas.create_text(
                width // 2,
                height // 2,
                text="Map preview unavailable",
                anchor="center",
                font=("Arial", 12),
            )

    def _open_selected_in_maps(self):
        """Reutilizamos el nuevo método load_route para abrir la ruta."""
        self.load_route()

    def load_route(self):
        """Abre Google Maps con la ruta actualmente seleccionada."""
        sel = self.routes_tv.selection()
        if not sel:
            messagebox.showwarning("Warning", "Please select a route first.")
            return

        self.current_route_id = self.route_rows.get(sel[0])
        if self.current_route_id is None:
            messagebox.showwarning("Warning", "Selected route ID not found.")
            return

        try:
            stops = get_route_stops(self.current_route_id)
        except Exception:
            messagebox.showinfo("Info", "No stops for this route.")
            return

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
