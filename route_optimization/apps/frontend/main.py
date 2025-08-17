import tkinter as tk
from tkinter import ttk
from apps.frontend.gui_app.views.dashboard_frame import DashboardFrame
from apps.frontend.gui_app.views.routes_frame import RoutesFrame
from apps.frontend.gui_app.views.orders_frame import OrderFrame
from apps.frontend.gui_app.views.configuration_frame import ConfigFrame
from apps.frontend.gui_app.views.user_frame import UserFrame

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DEMO Route and Logistics")
        self.geometry("1000x600") # to determine later
        self.config(bg="#f0f0f0")

        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)

        # ------- SidePanel ------------
        sidepanel = tk.Frame(self,bg="#2c3e50",width=200)
        sidepanel.grid(row=0,column=0,sticky="ns")
        sidepanel.grid_propagate(False) # set width

        # ---------- Navigation Buttoms -------------
        ttk.Button(sidepanel,text="Home Dashboard",command=lambda: self.show_frame("DashboardFrame")
                   ).pack(fill="x",pady=5,padx=10)
        ttk.Button(sidepanel,text="Manage Routes",command=lambda: self.show_frame("RoutesFrame")
                   ).pack(fill="x",pady=5,padx=10)
        ttk.Button(sidepanel,text="Order logs",command=lambda: self.show_frame("OrderFrame")
                   ).pack(fill="x",pady=5,padx=10)
        ttk.Button(sidepanel,text="Configuration",command=lambda: self.show_frame("ConfigFrame")
                   ).pack(fill="x",pady=5,padx=10)
        ttk.Button(sidepanel,text="User/Client",command=lambda: self.show_frame("UserFrame")
                   ).pack(fill="x",pady=5,padx=10)

        # views container
        container = tk.Frame(self,bg="#f0f0f0")
        container.grid(row=0,column=1,sticky="nsew")

        # frames dict
        self.frames = {}

        for F in (DashboardFrame,RoutesFrame,OrderFrame,ConfigFrame,UserFrame):
            frame = F(container,self)
            self.frames[F.__name__] = frame
            frame.grid(row=0,column=0,sticky="nsew")


        # Set the dashboard as default
        self.show_frame("DashboardFrame")


    def show_frame(self,name):
        frame = self.frames[name]
        frame.tkraise() # bring the frame to the front

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()