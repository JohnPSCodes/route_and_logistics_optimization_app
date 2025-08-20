import tkinter as tk
from tkinter import messagebox

class MenuBar:
    def __init__(self, master):
        self.master = master
        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.master)

        # --------- Files Menu ---------
        files_menu = tk.Menu(menu_bar, tearoff=0)
        files_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        files_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        files_menu.add_separator()
        files_menu.add_command(label="Exit", accelerator="Ctrl+Q", command=self.exit_app)

        # --------- Help Menu ---------
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help", command=self.show_help)
        help_menu.add_command(label="About", command=self.show_about)

        # --------- Config Menu ---------
        config_menu = tk.Menu(menu_bar, tearoff=0)
        config_menu.add_command(label="Option 1", command=lambda: self.show_option("Option 1"))
        config_menu.add_command(label="Option 2", command=lambda: self.show_option("Option 2"))
        config_menu.add_command(label="Option 3", command=lambda: self.show_option("Option 3"))
        config_menu.add_command(label="Option 4", command=lambda: self.show_option("Option 4"))

        # Add menus to the menubar
        menu_bar.add_cascade(label="Files", menu=files_menu)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        menu_bar.add_cascade(label="Config", menu=config_menu)

        # Attach menubar to the main window
        self.master.config(menu=menu_bar)

        # Optional: bind accelerators
        self.master.bind_all("<Control-n>", lambda e: self.new_file())
        self.master.bind_all("<Control-o>", lambda e: self.open_file())
        self.master.bind_all("<Control-q>", lambda e: self.exit_app())

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
