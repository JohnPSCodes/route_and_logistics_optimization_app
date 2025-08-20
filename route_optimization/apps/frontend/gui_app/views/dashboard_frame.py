import tkinter as tk
from tkinter import ttk

class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        
        # Title
        title = tk.Label(self, text="Dashboard", font=("Arial", 18, "bold"), bg="white")
        title.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")

        # Configure grid for responsiveness
        self.grid_rowconfigure(1, weight=1)  # row with cards
        self.grid_columnconfigure((0,1,2), weight=1, uniform="cards")

        # Sample cards container
        self.create_card(row=1, column=0, title="Total Orders", value="120")
        self.create_card(row=1, column=1, title="Active Routes", value="8")
        self.create_card(row=1, column=2, title="Pending Deliveries", value="23")

        # Lower area for charts or logs
        lower_frame = tk.Frame(self, bg="white")
        lower_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=20)
        self.grid_rowconfigure(2, weight=2)

        # Example: placeholder for a chart or table
        chart_placeholder = tk.Label(lower_frame, text="Chart / Table Placeholder", 
                                     bg="#f0f0f0", relief="groove")
        chart_placeholder.pack(fill="both", expand=True)

    def create_card(self, row, column, title, value):
        card = ttk.Frame(self, relief="ridge", padding=(20,10))
        card.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
        
        # Make card responsive
        self.grid_rowconfigure(row, weight=1)
        self.grid_columnconfigure(column, weight=1)

        # Card content
        title_label = tk.Label(card, text=title, font=("Arial", 12), fg="#555555")
        title_label.pack(anchor="w")
        value_label = tk.Label(card, text=value, font=("Arial", 24, "bold"), fg="#2c3e50")
        value_label.pack(anchor="center", pady=10)
