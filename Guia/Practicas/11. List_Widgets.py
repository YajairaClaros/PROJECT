#10 - Widgets de lista (ListBox y ComboBox)
import tkinter as tk
from tkinter import ttk  # ttk es necesario para usar Combobox

ventana = tk.Tk()
ventana.title("Widgets de lista")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# Los widgets de lista permiten mostrar múltiples opciones para que el usuario elija.
# - Listbox: muestra una lista de ítems donde se puede seleccionar uno o varios.
# - Combobox: una lista desplegable más compacta (estilo menú).

# ---------------------------- Listbox ----------------------------

etiqueta_lista = tk.Label(ventana, text="Selecciona un lenguaje:")
etiqueta_lista.pack()

# Creamos una Listbox
lista = tk.Listbox(ventana, height=5, selectmode=tk.SINGLE)  # selectmode puede ser MULTIPLE, EXTENDED, etc.

# Agregamos elementos a la lista
lenguajes = ["Python", "Java", "C++", "JavaScript", "Ruby"]
for lang in lenguajes:
    lista.insert(tk.END, lang)#Inserta un nuevo elemento (lang) al final del Listbox llamado lista.

lista.pack()

# Función que muestra el ítem seleccionado
def mostrar_seleccion_lista():
    seleccion = lista.curselection()  # Retorna una tupla con los índices seleccionados
    if seleccion:
        valor = lista.get(seleccion[0])
        etiqueta_resultado.config(text=f"Seleccionaste: {valor}")
    else:
        etiqueta_resultado.config(text="No hay selección.")

boton_lista = tk.Button(ventana, text="Mostrar selección", command=mostrar_seleccion_lista)
boton_lista.pack(pady=5)

# ---------------------------- Combobox ----------------------------

etiqueta_combo = tk.Label(ventana, text="Selecciona un país:")
etiqueta_combo.pack(pady=(20, 0))  # Espacio superior

# Creamos una Combobox
combo = ttk.Combobox(ventana, values=["El Salvador", "México", "Colombia", "Argentina"])
combo.pack()

# Función para mostrar selección del combobox
def mostrar_seleccion_combo(event):
    etiqueta_resultado.config(text=f"País seleccionado: {combo.get()}")

# Vinculamos evento de selección
combo.bind("<<ComboboxSelected>>", mostrar_seleccion_combo)

# ---------------------------- Etiqueta de salida ----------------------------

etiqueta_resultado = tk.Label(ventana, text="", fg="blue")
etiqueta_resultado.pack(pady=10)

ventana.mainloop()
