# maestros.py
import tkinter as tk
from tkinter import ttk

class Ver_Materias:
    def __init__(self, content_frame):
        self.content_frame = content_frame

    def mostrar(self):
        ttk.Label(self.content_frame, text="Materias", font=("Bookish", 16, "bold")).grid(row=1, column=0, columnspan=2, pady=(0, 10))

        # ---------------------- Entradas ----------------------
        self.Frame_entry = ttk.Frame(self.content_frame, style="White.TFrame")

        label_nombre = ttk.Label(self.Frame_entry, text="Nombre de la materia:")
        label_nombre.grid(row=0, column=0, sticky="e", pady=(20, 0))
        entry_nombre = ttk.Entry(self.Frame_entry, width=35, font=("Bookish", 12))
        entry_nombre.grid(row=0, column=1, sticky="w", pady=(20, 0))

        label_codigo = ttk.Label(self.Frame_entry, text="Código de la materia:")
        label_codigo.grid(row=1, column=0, sticky="e", pady=(20, 0))
        entry_codigo = ttk.Entry(self.Frame_entry, width=35, font=("Bookish", 12))
        entry_codigo.grid(row=1, column=1, sticky="w", pady=(20, 0))

        label_maestros = ttk.Label(self.Frame_entry, text="Maestros:")
        label_maestros.grid(row=2, column=0, sticky="e", pady=(20, 0))
        entry_maestros = ttk.Combobox(self.Frame_entry, width=35, values=["Mike", "Albert","Regi"], font=("Bookish", 12))
        entry_maestros.grid(row=2, column=1, sticky="w", pady=(20, 0))


        # Botón negro con texto blanco
        button_agregar_maestro = ttk.Button(self.Frame_entry, text="Agregar", style="Black.TButton")
        button_agregar_maestro.grid(row=2, column=2, pady=(20, 0), padx=(10, 0))

        self.Frame_entry.grid(column=0, row=2, columnspan=2)

        # ---------------------- Tabla Treeview ----------------------
        columnas = ("Materia", "Código", "Maestros", "Opciones")
        self.tree = ttk.Treeview(self.content_frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=200)

        self.tree.grid(row=3, column=0, columnspan=3, pady=20, padx=20, sticky="nsew")
        self.content_frame.grid_rowconfigure(3, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
