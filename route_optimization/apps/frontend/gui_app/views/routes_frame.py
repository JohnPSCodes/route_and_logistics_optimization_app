import tkinter as tk
from tkinter import ttk

class RoutesFrame(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white")

        # config main grid
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=0)
        self.grid_columnconfigure(0,weight=1)

        # Label upper title
        title_label = tk.Label(self,text="Routes",font=("Arial",18),bg="white")
        title_label.grid(row=0,column=0,sticky="nw",padx=10,pady=10)

        # Map container
        map_container = tk.Frame(self,bg="lightgray",width=800,height=450)
        map_container.grid(row=1,column=0,sticky="nsew",padx=40,pady=10)

        # Buttons container
        buttons_container = tk.Frame(self,bg="white")
        buttons_container.grid(row=2,column=0,sticky="ew",padx=10,pady=10)

        # buttons
        ttk.Button(buttons_container,text="Add waypoint(stop)").grid(row=0,column=0,padx=5)
        ttk.Button(buttons_container,text="Delete waypoint(stop)").grid(row=0,column=1,padx=5)
        ttk.Button(buttons_container,text="Load route").grid(row=0,column=2,padx=5)
        ttk.Button(buttons_container,text="See all routes").grid(row=1,column=0,padx=5)
        ttk.Button(buttons_container,text="Open MAP").grid(row=1,column=1,padx=5)
        ttk.Button(buttons_container,text="Assign route").grid(row=1,column=2,padx=5)