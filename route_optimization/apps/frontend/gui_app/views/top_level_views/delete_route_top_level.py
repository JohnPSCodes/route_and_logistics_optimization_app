
import tkinter as tk
from tkinter import ttk, messagebox
from apps.backend.services.routes import get_route, delete_route

class DeleteRouteTopLevel(tk.Toplevel):
    """
    Toplevel para confirmar la eliminación de una ruta.
    """
    def __init__(self, parent, route_id: int, refresh_callback=None):
        super().__init__(parent)
        self.title("Delete Route")
        self.geometry("360x160")
        self.resizable(False, False)

        self.route_id = route_id
        self.refresh_callback = refresh_callback

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

        # ---------- UI ----------
        container = ttk.Frame(self, padding=12)
        container.pack(fill="both", expand=True)

        msg = f"Are you sure you want to delete route:\n\n  {self.route.name} (ID: {self.route.id}) ?"
        ttk.Label(container, text=msg, justify="center", wraplength=320).pack(fill="x", pady=(0,12))

        btns = ttk.Frame(container)
        btns.pack(fill="x")
        btns.columnconfigure((0,1), weight=1)

        ttk.Button(btns, text="Delete", command=self.confirm_delete).grid(row=0, column=0, sticky="ew", padx=(0,6))
        ttk.Button(btns, text="Cancel", command=self.destroy).grid(row=0, column=1, sticky="ew", padx=(6,0))

    def confirm_delete(self):
        try:
            delete_route(self.route_id)
            messagebox.showinfo("Success", f"Route '{self.route.name}' deleted.")
            if callable(self.refresh_callback):
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete route:\n{e}")
