import tkinter as tk
from tkinter import ttk

# Crear ventana principal
root = tk.Tk()
root.title("Comparación: Tkinter clásico vs ttk")
root.geometry("500x300")
root.resizable(False, False)

# Crear frames para organizar los widgets
frame_classic = tk.LabelFrame(root, text="Tkinter clásico", padx=10, pady=10)
frame_classic.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

frame_ttk = tk.LabelFrame(root, text="ttk (moderno)", padx=10, pady=10)
frame_ttk.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Widgets Tkinter clásico
tk.Label(frame_classic, text="Etiqueta:").pack(anchor="w")
tk.Entry(frame_classic).pack(fill="x", pady=5)
tk.Button(frame_classic, text="Botón").pack(pady=5)

# Widgets ttk
ttk.Label(frame_ttk, text="Etiqueta:").pack(anchor="w")
ttk.Entry(frame_ttk).pack(fill="x", pady=5)
ttk.Button(frame_ttk, text="Botón").pack(pady=5)

# Extra: Combobox solo existe en ttk
ttk.Label(frame_ttk, text="Combobox:").pack(anchor="w", pady=(10, 0))
ttk.Combobox(frame_ttk, values=["Opción 1", "Opción 2", "Opción 3"]).pack(fill="x")

root.mainloop()
