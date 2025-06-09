#8 - Ventanas dinámicas
import tkinter as tk
from tkinter.ttk import Button

ventana = tk.Tk()
ventana.title("Ventanas dinámicas")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# "Ventanas dinámicas" no es un término oficial de Tkinter, pero se usa para describir
# interfaces que cambian durante la ejecución (mostrar, ocultar o modificar elementos),
# o que abren nuevas ventanas como Toplevel.
# El widget Toplevel permite crear una ventana nueva independiente de la principal.

def abrir_ventana_topLevel():
    ventana_toplevel = tk.Toplevel(ventana)  # Crea una nueva ventana secundaria
    ventana_toplevel.title("Ventana TopLevel")
    ventana_toplevel.geometry("300x200+100+100")

    # Podemos agregar elementos dentro de esa ventana
    label = tk.Label(ventana_toplevel, text="¡Soy una ventana nueva!")
    label.pack(pady=10)

    btn_cerrar = Button(ventana_toplevel, text="Cerrar", command=ventana_toplevel.destroy)
    btn_cerrar.pack(pady=5)

# Botón que abre la ventana dinámica
boton = Button(ventana, text="Abrir Ventana TopLevel", command=abrir_ventana_topLevel)
boton.pack(pady=20)

ventana.mainloop()
