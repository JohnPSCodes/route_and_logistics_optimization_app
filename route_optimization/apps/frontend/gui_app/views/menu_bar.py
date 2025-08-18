
import tkinter as tk

class MenuBar:
    def __init__(self,master):
        self.master = master
        self.create_menu()

    def create_menu(self):
        menu_bar =tk.Menu(self.master)

        # Menubar option [Files]
        files_menu = tk.Menu(menu_bar,tearoff=0)
        files_menu.add_command(label="New",command=...)
        files_menu.add_command(label="Open",command=...)
        files_menu.add_separator()
        files_menu.add_command(label="Exit",command=...)
        
        # Menubar option [Help]
        help_menu = tk.Menu(menu_bar,tearoff=0)
        help_menu.add_command(label="About",command=...)
        help_menu.add_command(label="Help",command=...)

        # Menubar option [Config]
        config_menu = tk.Menu(menu_bar,tearoff=0)
        config_menu.add_command(label="Option_1",command=...)
        config_menu.add_command(label="Option_2",command=...)
        config_menu.add_command(label="Option_3",command=...)
        config_menu.add_command(label="Option_4",command=...)

        # add to the menubar
        menu_bar.add_cascade(label="Files",menu=files_menu)
        menu_bar.add_cascade(label="Help",menu=help_menu)
        menu_bar.add_cascade(label="Config",menu=config_menu)

        # assign menubar to the main window
        self.master.config(menu=menu_bar)