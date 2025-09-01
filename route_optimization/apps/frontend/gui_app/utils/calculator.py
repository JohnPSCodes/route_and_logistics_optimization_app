import tkinter as tk
from apps.frontend.gui_app.utils.windows_utils import center_window

class Calculator:
    BUTTON_BG = "#2c3e50"
    BUTTON_FG = "#FFFFFF"
    OP_BG = "#36373A"
    OP_FG = "#FFFFFF"
    ENTRY_BG = "#ECECEC"
    ENTRY_FG = "#333"
    FONT_ENTRY = ("Helvetica", 24)
    FONT_BUTTON = ("Helvetica", 18, "bold")

    def __init__(self, master=None):
        self.master = master
        self.create_window()

    def create_window(self):
        self.calc_window = tk.Toplevel(self.master)
        self.calc_window.title("Calculator")
        self.calc_window.geometry("400x500")
        self.calc_window.resizable(False, False)
        center_window(self.calc_window)

        # Result input
        self.entry = tk.Entry(
            self.calc_window,
            width=16,
            font=self.FONT_ENTRY,
            borderwidth=2,
            relief="ridge",
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            justify="right"
        )
        self.entry.grid(row=0, column=0, columnspan=4, pady=10, padx=10, ipady=10)

        self.create_buttons()

    def create_buttons(self):
        buttons = [
            ('C', 1, 0), ('Del', 1, 1), ('%', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2)
        ]

        for (text, row, col) in buttons:
            if text in '+-*/=%':
                bg_color = self.OP_BG
                fg_color = self.OP_FG
            elif text in ('C', 'Del'):
                bg_color = "#E7901F"  # Orange for delete
                fg_color = "#FFFFFF"
            else:
                bg_color = self.BUTTON_BG
                fg_color = self.BUTTON_FG

            b = tk.Button(
                self.calc_window,
                text=text,
                width=5,
                height=2,
                font=self.FONT_BUTTON,
                bg=bg_color,
                fg=fg_color,
                activebackground="#D32F2F" if text in ('C', 'Del') else "#388E3C",
                command=lambda val=text: self.click_button(val)
            )
            b.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

        # Expand buttons
        for i in range(6):
            self.calc_window.rowconfigure(i, weight=1)
        for i in range(4):
            self.calc_window.columnconfigure(i, weight=1)

    def click_button(self, value):
        if value == "=":
            try:
                result = eval(self.entry.get())
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, str(result))
            except Exception:
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, "Error")
        elif value == "C":
            self.entry.delete(0, tk.END)  # Clear all
        elif value == "Del":
            self.entry.delete(len(self.entry.get())-1, tk.END)  # Delete last character
        else:
            self.entry.insert(tk.END, value)
