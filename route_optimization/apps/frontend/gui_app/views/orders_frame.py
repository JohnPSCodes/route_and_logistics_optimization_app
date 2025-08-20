import tkinter as tk
from tkinter import ttk
import requests
from route_optimization.config_user import JWT_TOKEN, API_URL_ORDERS
from apps.frontend.gui_app.views.top_level_views.create_order_top_level import CreateOrderTopLevel
from apps.frontend.gui_app.views.top_level_views.edit_order_top_level import EditOrderTopLevel
from apps.frontend.gui_app.views.top_level_views.delete_order_top_level import DeleteOrderTopLevel 

class OrderFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")

        # ----------------- Label -----------------
        tk.Label(
            self,
            text="Orders Management",
            font=("Arial", 18),
            bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20, sticky="n")

        # ----------------- Container -----------------
        container = tk.Frame(self, bg="white")
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

        # Permitir que el container crezca
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # ----------------- Treeview -----------------
        self.order_tree = ttk.Treeview(
            container,
            columns=(
                "id", "customer_name", "address", "latitude", "longitude",
                "priority", "delivery_window_start", "delivery_window_end", "status"
            ),
            show="headings"
        )

        # ----------------- Scrollbars -----------------
        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.order_tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.order_tree.xview)
        self.order_tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Posicionar Treeview y scrollbars
        self.order_tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        scrollbar_x.grid(row=1, column=0, sticky="ew")

        # ----------------- Headings -----------------
        headings = {
            "id": "ID",
            "customer_name": "Customer Name",
            "address": "Address",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "priority": "Priority",
            "delivery_window_start": "Delivery Start",
            "delivery_window_end": "Delivery End",
            "status": "Status"
        }
        for col, text in headings.items():
            self.order_tree.heading(col, text=text)

        # -----------------Button -----------------
        button_frame = tk.Frame(self, bg="white")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        ttk.Button(button_frame, text="Create Order", command=self.create_order).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Order", command=self.edit_order).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Order", command=self.delete_order).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.load_orders_from_db).pack(side="left", padx=5)

        # ----------------- Bind resize -----------------
        self.order_tree.bind("<Configure>", self._resize_columns)

        # ----------------- Load initial data -----------------
        self.load_orders_from_db()

    def load_orders_from_db(self):
        headers = {"Authorization": f"Bearer {JWT_TOKEN}"}
        try:
            response = requests.get(API_URL_ORDERS, headers=headers, timeout=5)
            if response.status_code == 200:
                orders = response.json()
                # clean treeview
                for iid in self.order_tree.get_children():
                    self.order_tree.delete(iid)
                # Insert data
                for order in orders:
                    self.order_tree.insert(
                        "",
                        "end",
                        values=(
                            order.get("id"),
                            order.get("customer_name"),
                            order.get("address"),
                            order.get("latitude"),
                            order.get("longitude"),
                            order.get("priority"),
                            order.get("delivery_window_start"),
                            order.get("delivery_window_end"),
                            order.get("status"),
                        )
                    )
        except requests.RequestException as e:
            print("Error loading orders:", e)

    def _resize_columns(self, event):
        """Adjust columns dynamically, some are fixed"""
        total_width = event.width

        # Columnas con ancho fijo
        fixed_columns = {"id": 80, "priority": 80, "status": 100}

        # Columnas dinámicas y sus pesos
        dynamic_weights = {
            "customer_name": 2,
            "address": 3,
            "latitude": 1,
            "longitude": 1,
            "delivery_window_start": 2,
            "delivery_window_end": 2,
        }

        used_width = sum(fixed_columns.values())
        remaining_width = max(total_width - used_width, 200)
        total_weight = sum(dynamic_weights.values())

        # Ajustar columnas fijas
        for col, width in fixed_columns.items():
            self.order_tree.column(col, width=width, anchor="center")

        # Ajustar columnas dinámicas
        for col, weight in dynamic_weights.items():
            new_width = int(remaining_width * (weight / total_weight))
            self.order_tree.column(col, width=max(new_width, 80), anchor="w")

    def create_order(self):
        CreateOrderTopLevel(self, callback=self.load_orders_from_db)

    def edit_order(self):
        selected = self.order_tree.selection()
        if not selected:
            tk.messagebox.showwarning("No Selection", "Please select an order to edit")
            return
        order_values = self.order_tree.item(selected[0])["values"]
        order_data = {
            "id": order_values[0],
            "customer_name": order_values[1],
            "address": order_values[2],
            "latitude": order_values[3],
            "longitude": order_values[4],
            "priority": order_values[5],
            "delivery_window_start": order_values[6],
            "delivery_window_end": order_values[7],
            "status": order_values[8]
        }
        EditOrderTopLevel(self, order_data, callback=self.load_orders_from_db)

    def delete_order(self):
        selected = self.order_tree.selection()
        if not selected:
            tk.messagebox.showwarning("Warning", "Please select an order to delete.")
            return
        order_data = self.order_tree.item(selected[0])['values']
        order_dict = {
            "id": order_data[0],
            "customer_name": order_data[1]
        }
        DeleteOrderTopLevel(self, order_dict, callback=self.load_orders_from_db)