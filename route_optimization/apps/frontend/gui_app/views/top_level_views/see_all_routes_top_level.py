# apps/frontend/gui_app/views/top_level_views/see_all_routes_top_level.py
import tkinter as tk
from tkinter import ttk, messagebox
from apps.backend.services.routes import get_all_route
from apps.frontend.gui_app.views.top_level_views.add_route_top_level import AddRouteTopLevel
from apps.frontend.gui_app.views.top_level_views.edit_route_top_level import EditRouteTopLevel
from apps.frontend.gui_app.views.top_level_views.delete_route_top_level import DeleteRouteTopLevel
from apps.frontend.gui_app.utils.windows_utils import center_window

class SeeAllRoutesTopLevel(tk.Toplevel):
    def __init__(self, parent, refresh_callback=None):
        super().__init__(parent)
        self.title("Manage Routes")
        self.geometry("600x400")
        self.refresh_callback = refresh_callback
        center_window(self)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("id", "name", "planned_date"), show="headings")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Route Name")
        self.tree.heading("planned_date", text="Planned Date")

        self.tree.column("id", width=50, anchor="center")
        self.tree.column("name", width=300)
        self.tree.column("planned_date", width=200, anchor="center")

        # Botones
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", pady=5)

        ttk.Button(button_frame, text="Add Route", command=self.add_route).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Route", command=self.edit_route).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Route", command=self.delete_route).pack(side="left", padx=5)

        self.load_routes()

    def load_routes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        routes = get_all_route()
        for r in routes:
            self.tree.insert("", "end", values=(r.id, r.name, r.planned_date))

    def add_route(self):
        # pasa el user_id válido de tu sesión/usuario actual
        AddRouteTopLevel(self, created_by_id=1, refresh_callback=self.load_routes)

    def edit_route(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a route to edit.")
            return
        route_id = self.tree.item(selected, "values")[0]
        EditRouteTopLevel(self, route_id=int(route_id), refresh_callback=self.load_routes)

    def delete_route(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a route to delete")
            return
        route_id = self.tree.item(selected[0], "values")[0]
        DeleteRouteTopLevel(self, route_id=route_id, refresh_callback=self.load_routes)
