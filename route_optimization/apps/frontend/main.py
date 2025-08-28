import tkinter as tk
from tkinter import ttk
from datetime import datetime
from apps.frontend.resources.resources import load_logo
from apps.frontend.gui_app.views.dashboard_frame import DashboardFrame
from apps.frontend.gui_app.views.routes_frame import RoutesFrame
from apps.frontend.gui_app.views.orders_frame import OrderFrame
from apps.frontend.gui_app.views.configuration_frame import ConfigFrame
from apps.frontend.gui_app.views.user_frame import UserFrame
from apps.frontend.gui_app.views.menu_bar import MenuBar
from apps.frontend.gui_app.utils.windows_utils import center_window, on_resize


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DEMO Route and Logistics")
        self.geometry("1235x600")
        self.minsize(1235, 600)
        self.maxsize(1235, 600)
        self.config(bg="#f0f0f0")

        # --------- MenuBar --------
        MenuBar(self)

        # Configuración de la cuadrícula principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)  # Footer (status bar)

        # ------- SidePanel ------------
        sidepanel = tk.Frame(self, bg="#2c3e50", width=150)
        sidepanel.grid(row=0, column=0, sticky="ns")
        sidepanel.grid_propagate(False)

        sidepanel.grid_rowconfigure(0, weight=1)
        sidepanel.grid_rowconfigure(1, weight=1)
        sidepanel.grid_columnconfigure(0, weight=1)

        # ------- Logo ----------
        logo_label = load_logo(width=100, height=100)
        logo_label.grid(row=0, column=0, pady=(10), sticky="n")

        # ------- Navigation Buttons ----------
        buttons_frame = tk.Frame(sidepanel, bg="#2c3e50")
        buttons_frame.grid(row=1, column=0, sticky="n", pady=(410, 5))
        buttons_frame.grid_columnconfigure(0, weight=1)

        buttons = [
            ("Home Dashboard", "DashboardFrame"),
            ("Manage Routes", "RoutesFrame"),
            ("Order logs", "OrderFrame"),
            ("Configuration", "ConfigFrame"),
            ("User/Client", "UserFrame")
        ]

        for i, (text, frame_name) in enumerate(buttons):
            btn = ttk.Button(buttons_frame, text=text, command=lambda f=frame_name: self.show_frame(f))
            btn.grid(row=i, column=0, sticky="ew", pady=(5, 0), padx=10)

        # ------- Views Container ----------
        container = tk.Frame(self, bg="#f0f0f0")
        container.grid(row=0, column=1, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # ------- Frames Dict ----------
        self.frames = {}
        for F in (DashboardFrame, RoutesFrame, OrderFrame, ConfigFrame, UserFrame):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # ------- Status Bar (Footer) ----------
        status_frame = tk.Frame(self, bg="#2c3e50")
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew")

        # 3 secciones: izquierda, centro, derecha
        self.user_label = tk.Label(status_frame, text="Usuario: Johnpscodes", bg="#2c3e50", fg="white", anchor="w", padx=10)
        self.user_label.pack(side="left")

        self.connection_label = tk.Label(status_frame, text="Conectado ✅", bg="#2c3e50", fg="white")
        self.connection_label.pack(side="left", padx=20)

        self.version_label = tk.Label(status_frame, text="Versión 1.0.0", bg="#2c3e50", fg="white")
        self.version_label.pack(side="left", padx=20)

        self.clock_label = tk.Label(status_frame, text="", bg="#2c3e50", fg="white", anchor="e", padx=10)
        self.clock_label.pack(side="right")

        self.update_clock()  # Inicia el reloj

        # Default frame
        self.show_frame("DashboardFrame")
        center_window(self)  # Centers the window

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)  # Actualiza cada segundo


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
