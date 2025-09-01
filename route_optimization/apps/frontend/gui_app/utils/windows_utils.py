
import tkinter as tk

def center_window(win):
    """
    Center a window (Tk or Toplevel) on screen,
    calculating its current size automatically.
    """
    win.update_idletasks()  # ensure winfo_width/height contain correct values

    width = win.winfo_width()
    height = win.winfo_height()
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    win.geometry(f"+{x}+{y}")


def on_resize(event, target):
    """
    Event to capture the dynamic size of a window.
    
    event  : Tkinter <Configure> event
    target : window object (Tk or Toplevel) being monitored
    """
    new_size = (event.width, event.height)
    if not hasattr(target, "current_size"):
        target.current_size = (event.width, event.height)
        return
    if new_size != target.current_size:
        target.current_size = new_size
        print(f"Dynamic size {target.__class__.__name__}: {event.width}x{event.height}")

# Example of on_resize usage:
# Dynamic size monitoring, placed on the window to be inspected
#     self.current_size = (self.winfo_width(), self.winfo_height())
#     self.bind("<Configure>", lambda e: on_resize(e, self))