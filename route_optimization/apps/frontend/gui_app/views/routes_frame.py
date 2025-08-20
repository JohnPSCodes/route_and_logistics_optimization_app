import tkinter as tk
from tkinter import ttk
from apps.frontend.resources.google_maps import get_static_map
from route_optimization.config_user import GOOGLE_API_KEY

class RoutesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        # ---------- Main grid configuration ----------
        self.grid_rowconfigure(1, weight=1)  # map container grows
        self.grid_rowconfigure(2, weight=0)  # buttons container does not grow
        self.grid_columnconfigure(0, weight=1)

        # ---------- Top label ----------
        title_label = tk.Label(self, text="Routes", font=("Arial", 18), bg="white")
        title_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # ---------- Map container ----------
        self.map_container = tk.Frame(self, bg="lightgray")
        self.map_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Make the map container expandable
        self.map_container.grid_rowconfigure(0, weight=1)
        self.map_container.grid_columnconfigure(0, weight=1)

        # Placeholder for map widget or canvas
        self.map_canvas = tk.Canvas(self.map_container, bg="lightblue")
        self.map_canvas.grid(row=0, column=0, sticky="nsew")

        # ---------- Buttons container ----------
        buttons_container = tk.Frame(self, bg="white")
        buttons_container.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        buttons_container.grid_columnconfigure((0, 1, 2), weight=1)  # distribute space evenly

        # ---------- Buttons ----------
        ttk.Button(buttons_container, text="Add waypoint(stop)").grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Delete waypoint(stop)").grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Load route").grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="See all routes").grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Open MAP").grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        ttk.Button(buttons_container, text="Assign route").grid(row=1, column=2, padx=5, pady=5, sticky="ew")
        
        self.map_canvas.bind("<Configure>", lambda e: self.load_map())

    def load_map(self):
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()
        self.map_img_tk = get_static_map(
        center="18.61278955260962, -68.71589989505831",
        zoom=12,
        size=(width, height),
        markers=[(18.61278955260962, -68.71589989505831)],
        api_key=GOOGLE_API_KEY,
        scale=1
    )
        if self.map_img_tk:
            self.map_canvas.delete("all")
            self.map_canvas.create_image(0, 0, anchor="nw", image=self.map_img_tk)
        