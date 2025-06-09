#16 - Widgets de tiempo (Calendar y DatEntry)
import tkinter as tk
from tkcalendar import Calendar, DateEntry  # Necesitas instalar tkcalendar: pip install tkcalendar

ventana = tk.Tk()
ventana.title("Widgets de tiempo")
ventana.geometry("700x600")

# INTRODUCCIÓN:
# Tkinter no incluye widgets de calendario o selector de fecha nativos.
# Por eso se utiliza la librería externa 'tkcalendar' que añade dos widgets principales:
# Calendar: para mostrar un calendario completo.
# DateEntry: para seleccionar fechas en un cuadro de texto desplegable con calendario.

# --------------------- Widget Calendar ---------------------

cal = Calendar(ventana, selectmode="day", year=2025, month=6, day=8)
cal.pack(pady=20)

# --------------------- Widget DateEntry ---------------------

fecha_entrada = DateEntry(ventana, width=12, background='darkblue',
                          foreground='white', borderwidth=2)
fecha_entrada.pack(pady=10)

# --------------------- Función para mostrar la fecha seleccionada ---------------------

def mostrar_fecha():
    seleccion = fecha_entrada.get()
    etiqueta_fecha.config(text=f"Fecha seleccionada: {seleccion}")

boton_mostrar = tk.Button(ventana, text="Mostrar fecha seleccionada", command=mostrar_fecha)
boton_mostrar.pack(pady=10)

etiqueta_fecha = tk.Label(ventana, text="")
etiqueta_fecha.pack()

ventana.mainloop()
