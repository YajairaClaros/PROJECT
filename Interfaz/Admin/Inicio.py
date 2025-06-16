# inicio.py
import tkinter as tk
from tkinter import ttk

class Ver_Inicio:
    def __init__(self, content_frame):
        self.content_frame = content_frame

    def mostrar(self):
        try:
            with open("../Usuario_Logueado.txt", "r") as f:
                user = f.read().strip()
        except:
            with open("Usuario_Logueado.txt", "r") as f:
                    user = f.read().strip()

        self.label_welcome = ttk.Label(self.content_frame, text=f"¡Bienvenido {user}!", style="White.TLabel", font=("Bookish", 14, "bold"))
        self.label_welcome.grid(row=1, column=0, columnspan=2, pady=10)

        self.content_frame.grid_columnconfigure(1, weight=1)
