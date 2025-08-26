
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from apps.backend.services.routes import get_route, update_route
from apps.frontend.gui_app.utils.windows_utils import center_window

class EditRouteTopLevel(tk.Toplevel):
    """
    Toplevel para editar una ruta existente.

    Requiere:
        - route_id (int): ID de la ruta a editar
        - refresh_callback (callable|None): función para refrescar la UI del padre tras guardar
    """
    STATUSES = ["planned", "in_progress", "completed"]

    def __init__(self, parent, route_id: int, refresh_callback=None):
        super().__init__(parent)
        self.title("Edit Route")
        self.geometry("420x260")
        self.resizable(False, False)
        self.route_id = route_id
        self.refresh_callback = refresh_callback
        center_window(self)

        # Modal
        self.transient(parent)
        self.grab_set()

        # ---------- Load route ----------
        try:
            self.route = get_route(route_id)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load route: {e}")
            self.destroy()
            return

        # ---------- Form ----------
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        # Name
        ttk.Label(container, text="Route Name:").grid(row=0, column=0, sticky="w", pady=(0,6))
        self.var_name = tk.StringVar(value=self.route.name)
        self.entry_name = ttk.Entry(container, textvariable=self.var_name)
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=(8,0), pady=(0,6))

        # Planned Date
        ttk.Label(container, text="Planned Date:").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_date = DateEntry(container, date_pattern="yyyy-mm-dd")
        if self.route.planned_date:
            self.entry_date.set_date(self.route.planned_date)
        self.entry_date.grid(row=1, column=1, sticky="w", padx=(8,0), pady=6)

        # Status
        ttk.Label(container, text="Status:").grid(row=2, column=0, sticky="w", pady=6)
        self.var_status = tk.StringVar(value=self.route.status)
        self.combo_status = ttk.Combobox(container, state="readonly",
                                         values=self.STATUSES, textvariable=self.var_status)
        self.combo_status.grid(row=2, column=1, sticky="w", padx=(8,0), pady=6)

        # Layout grid
        container.columnconfigure(0, weight=0)
        container.columnconfigure(1, weight=1)

        # ---------- Buttons ----------
        btns = ttk.Frame(container)
        btns.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(12,0))
        btns.columnconfigure((0,1), weight=1)

        ttk.Button(btns, text="Save", command=self.save_changes).grid(row=0, column=0, sticky="ew", padx=(0,6))
        ttk.Button(btns, text="Cancel", command=self.destroy).grid(row=0, column=1, sticky="ew", padx=(6,0))

        # Focus inicial y binding Enter
        self.entry_name.focus_set()
        self.bind("<Return>", lambda e: self.save_changes())

    # ---------- Actions ----------
    def save_changes(self):
        name = self.var_name.get().strip()
        planned_date = self.entry_date.get_date()
        status = self.var_status.get()

        if not name:
            messagebox.showwarning("Validation", "Route Name is required.")
            self.entry_name.focus_set()
            return
        if status not in self.STATUSES:
            messagebox.showwarning("Validation", "Invalid status.")
            return

        data = {
            "name": name,
            "planned_date": planned_date,
            "status": status
        }

        try:
            route = update_route(self.route_id, data)
            messagebox.showinfo("Success", f"Route '{route.name}' updated.")
            if callable(self.refresh_callback):
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update route:\n{e}")
