import tkinter as tk
from tkinter import ttk, messagebox
from django.utils import timezone
from apps.backend.services.stops import update_stop
from apps.frontend.gui_app.utils.windows_utils import center_window

class EditStopTopLevel(tk.Toplevel):
    def __init__(self, parent, stop, refresh_callback):
        super().__init__(parent)
        self.title(f"Edit Stop #{stop.stop_order}")
        self.geometry("400x250")
        self.stop = stop
        self.refresh_callback = refresh_callback
        center_window(self)

        # ---------- Info ----------
        tk.Label(self, text=f"Customer: {stop.order.customer_name}", font=("Arial", 12, "bold")).pack(pady=10)

        # Estado actual
        self.delivered_var = tk.BooleanVar(value=stop.delivered)
        ttk.Checkbutton(self, text="Delivered", variable=self.delivered_var).pack(pady=10)

        # ETA
        tk.Label(self, text=f"ETA: {stop.estimated_arrival.strftime('%Y-%m-%d %H:%M')}").pack(pady=5)

        # Lat/Lng
        tk.Label(self, text=f"Lat: {stop.order.latitude}, Lng: {stop.order.longitude}").pack(pady=5)

        # ---------- Botones ----------
        button_frame = tk.Frame(self)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Save", command=self.save_changes).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.destroy).grid(row=0, column=1, padx=5)

    def save_changes(self):
        try:
            delivered_now = self.delivered_var.get()
            data = {"delivered": delivered_now}

            if delivered_now:
                data["delivery_time"] = timezone.now()
            else:
                data["delivery_time"] = None

            update_stop(self.stop.id, data)

            messagebox.showinfo("Success", "Stop updated successfully.")
            self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Could not update stop: {e}")
