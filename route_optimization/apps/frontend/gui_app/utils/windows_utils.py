
import tkinter as tk

def center_window(win):
    """
    Center a window(tk or toplevel) on screen,
    calculating automatically its current size
    """
    win.update_idletasks() # ensure winfo_width/height contain correct values

    width = win.winfo_width()
    height = win.winfo_height()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = (screen_width // 2 ) - (width // 2)
    y = (screen_height // 2 ) - (height // 2)
    
    win.geometry(f"+{x}+{y}")


def on_resize(event, target):
    """
    Evento para capturar tamaño dinámico de una ventana.
    
    event  : evento <Configure> de Tkinter
    target : objeto ventana (Tk o Toplevel) que se está monitoreando
    """
    new_size = (event.width, event.height)
    if not hasattr(target, "current_size"):
        target.current_size = (event.width, event.height)
        return
    if new_size != target.current_size:
        target.current_size = new_size
        print(f"Tamaño dinámico {target.__class__.__name__}: {event.width}x{event.height}")

# on_resize use:
# Monitoreo de tamaño dinámico, colocado en la ventana a inspeccionar
    # self.current_size = (self.winfo_width(), self.winfo_height())
    # self.bind("<Configure>", lambda e: on_resize(e, self))