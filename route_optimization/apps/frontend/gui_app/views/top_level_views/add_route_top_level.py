
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import date
from apps.backend.services.routes import create_route
from apps.frontend.gui_app.utils.windows_utils import center_window

class AddRouteTopLevel(tk.Toplevel):
    """
    Toplevel para crear una nueva ruta.

    Requiere:
        - created_by_id (int): ID del usuario creador (FK).
        - refresh_callback (callable|None): función para refrescar la UI del padre tras guardar.
    """
    STATUSES = ["planned", "in_progress", "completed"]

    def __init__(self, parent, created_by_id: int, refresh_callback=None):
        super().__init__(parent)
        self.title("Add Route")
        self.geometry("420x260")
        self.resizable(False, False)
        self.created_by_id = created_by_id
        self.refresh_callback = refresh_callback
        center_window(self)

        # Opcional: comportamiento modal
        self.transient(parent)
        self.grab_set()

        # ---------- Form ----------
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        # Name
        ttk.Label(container, text="Route Name:").grid(row=0, column=0, sticky="w", pady=(0,6))
        self.var_name = tk.StringVar()
        self.entry_name = ttk.Entry(container, textvariable=self.var_name)
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=(8,0), pady=(0,6))

        # Planned Date
        ttk.Label(container, text="Planned Date:").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_date = DateEntry(container, date_pattern="yyyy-mm-dd")
        self.entry_date.set_date(date.today())
        self.entry_date.grid(row=1, column=1, sticky="w", padx=(8,0), pady=6)

        # Status
        ttk.Label(container, text="Status:").grid(row=2, column=0, sticky="w", pady=6)
        self.var_status = tk.StringVar(value=self.STATUSES[0])
        self.combo_status = ttk.Combobox(container, state="readonly",
                                         values=self.STATUSES, textvariable=self.var_status)
        self.combo_status.grid(row=2, column=1, sticky="w", padx=(8,0), pady=6)

        # Created by (informativo)
        ttk.Label(container, text=f"Created by (user id):").grid(row=3, column=0, sticky="w", pady=6)
        ttk.Label(container, text=str(self.created_by_id)).grid(row=3, column=1, sticky="w", padx=(8,0), pady=6)

        # Layout grid
        container.columnconfigure(0, weight=0)
        container.columnconfigure(1, weight=1)

        # ---------- Buttons ----------
        btns = ttk.Frame(container)
        btns.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12,0))
        btns.columnconfigure((0,1), weight=1)

        ttk.Button(btns, text="Save", command=self.save_route).grid(row=0, column=0, sticky="ew", padx=(0,6))
        ttk.Button(btns, text="Cancel", command=self.destroy).grid(row=0, column=1, sticky="ew", padx=(6,0))

        # Focus inicial y binding Enter
        self.entry_name.focus_set()
        self.bind("<Return>", lambda e: self.save_route())

    # ---------- Actions ----------
    def save_route(self):
        name = self.var_name.get().strip()
        planned_date = self.entry_date.get_date()
        status = self.var_status.get()

        # Validaciones básicas
        if not name:
            messagebox.showwarning("Validation", "Route Name is required.")
            self.entry_name.focus_set()
            return
        if status not in self.STATUSES:
            messagebox.showwarning("Validation", "Invalid status.")
            return
        if not isinstance(self.created_by_id, int):
            messagebox.showerror("Error", "created_by_id is invalid or missing.")
            return

        data = {
            "name": name,
            "planned_date": planned_date,
            "status": status,
            "created_by_id": self.created_by_id
        }

        try:
            route = create_route(data)
            messagebox.showinfo("Success", f"Route '{route.name}' created for {route.planned_date}.")
            if callable(self.refresh_callback):
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not create route:\n{e}")
