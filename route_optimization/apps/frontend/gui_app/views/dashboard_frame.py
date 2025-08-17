import tkinter as tk
from tkinter import ttk

class DashboardFrame(tk.Frame):
    def __init__(self,parent,controller):
        super().__init__(parent,bg="white")
        tk.Label(self,text="Dashboard",font=("Arial",18),bg="white").pack(pady=20)