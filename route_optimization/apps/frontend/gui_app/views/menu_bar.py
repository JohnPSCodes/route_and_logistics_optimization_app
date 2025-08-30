import tkinter as tk
from tkinter import messagebox
from apps.frontend.gui_app.utils.calculator import Calculator  # Importamos la calculadora

class MenuBar:
    def __init__(self, master):
        self.master = master
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)

        # Files Menu
        files_menu = tk.Menu(menu_bar, tearoff=0)
        files_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        files_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        files_menu.add_separator()
        files_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_app)

        # Utilities Menu
        utilities_menu = tk.Menu(menu_bar, tearoff=0)
        utilities_menu.add_command(label="Calculator", command=lambda: Calculator(self.master))
        utilities_menu.add_command(label="Unit Converter", command=self.unit_converter)

        # Help Menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

        # Config Menu
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(label="Option 1", command=lambda: self.show_option("Option 1"))

        menu_bar.add_cascade(label="Files", menu=files_menu)
        menu_bar.add_cascade(label="Utilities", menu=utilities_menu)
        menu_bar.add_cascade(label="Config", menu=config_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=menu_bar)

    # --------- Placeholder methods ---------
    def new_file(self):
        messagebox.showinfo("New", "New file action triggered.")

    def open_file(self):
        messagebox.showinfo("Open", "Open file action triggered.")

    def exit_app(self):
        self.master.quit()

    def show_help(self):
        messagebox.showinfo("Help", "Help information goes here.")

    def show_about(self):
        messagebox.showinfo("About", "Route and Logistics App v1.0")

    def show_option(self, option_name):
        messagebox.showinfo(option_name, f"{option_name} selected.")

    def unit_converter(self):
        messagebox.showinfo("Unit Converter", "Coming soon!")
