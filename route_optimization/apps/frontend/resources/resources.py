import os
from PIL import Image, ImageTk 
import tkinter as tk

# -------- Paths --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "c15be2c62961ad37577a4ae17af24c1c.jpg")  # coloca tu logo aquí

# -------- Functions to load images --------
def load_logo(width=100, height=100, bg_color="#2c3e50"):
    """Load and resize the logo image, return a Tkinter Label"""
    if not os.path.exists(LOGO_PATH):
        raise FileNotFoundError(f"Logo not found at {LOGO_PATH}")

    img = Image.open(LOGO_PATH)
    img = img.resize((width, height), Image.LANCZOS)
    photo = ImageTk.PhotoImage(img)

    label = tk.Label(bg=bg_color, image=photo)
    label.image = photo  # keep reference to prevent garbage collection
    return label
