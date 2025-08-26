import tkinter as tk
from tkinter import ttk, messagebox
from apps.backend.services.stops import delete_stop, get_route_stops
from apps.frontend.gui_app.utils.windows_utils import center_window

class DeleteStopTopLevel(tk.Toplevel):
    def __init__(self, parent, route_id, refresh_callback=None):
        super().__init__(parent)
        self.title("Delete Waypoint")
        self.geometry("400x300")
        self.route_id = route_id
        self.refresh_callback = refresh_callback
        center_window(self)

        ttk.Label(self, text="Select Stop to Delete:").pack(pady=10)

        # Lista de stops en Combobox
        self.stops = get_route_stops(route_id)
        self.stop_map = {f"{s.stop_order} - {s.order.customer_name}": s.id for s in self.stops}
        self.stop_var = tk.StringVar()
        self.combobox_stops = ttk.Combobox(self, values=list(self.stop_map.keys()), textvariable=self.stop_var)
        self.combobox_stops.pack(fill="x", padx=20)

        # Botones
        frame_buttons = tk.Frame(self)
        frame_buttons.pack(pady=20, fill="x")
        ttk.Button(frame_buttons, text="Delete", command=self.delete_selected_stop).pack(side="left", expand=True, padx=10)
        ttk.Button(frame_buttons, text="Cancel", command=self.destroy).pack(side="right", expand=True, padx=10)

    def delete_selected_stop(self):
        selected = self.stop_var.get()
        if not selected:
            messagebox.showwarning("Warning", "Please select a stop to delete.")
            return

        stop_id = self.stop_map[selected]

        try:
            delete_stop(stop_id)
            messagebox.showinfo("Success", f"Stop '{selected}' deleted!")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
