#10 - Widgets de texto (Text y ScrolledText)
import tkinter as tk
from tkinter import scrolledtext  # Importamos el widget con scroll incorporado

ventana = tk.Tk()
ventana.title("Widgets de texto")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# Tkinter ofrece widgets para trabajar con bloques grandes de texto.
# - Text: permite ingresar, mostrar y editar múltiples líneas de texto.
# - ScrolledText: es una versión mejorada del Text que incluye una barra de desplazamiento vertical.

# -------------------- Widget Text (sin scroll) --------------------

etiqueta1 = tk.Label(ventana, text="Caja de texto simple (Text):")
etiqueta1.pack()

# Creamos el widget Text. width=40 = columnas, height=5 = filas de texto visibles
texto_simple = tk.Text(ventana, width=40, height=5)
texto_simple.pack(pady=10)

# Insertamos texto de ejemplo
texto_simple.insert(tk.END, "Aquí puedes escribir varias líneas de texto.\nEs editable.")

# -------------------- Widget ScrolledText --------------------

etiqueta2 = tk.Label(ventana, text="Caja de texto con scroll (ScrolledText):")
etiqueta2.pack()

# ScrolledText ya viene con barra de desplazamiento vertical automática
texto_scroll = scrolledtext.ScrolledText(ventana, width=40, height=10)
texto_scroll.pack(pady=10)

# Insertamos texto de ejemplo
texto_scroll.insert(tk.END, "Este widget permite desplazarte verticalmente cuando el contenido excede el tamaño.\n" * 5)

# -------------------- Botón para mostrar contenido --------------------

def mostrar_contenido():
    contenido = texto_scroll.get("1.0", tk.END)  # Obtenemos todo el texto desde la línea 1, carácter 0 hasta el final
    etiqueta_resultado.config(text="Contenido obtenido:\n" + contenido)

boton = tk.Button(ventana, text="Mostrar contenido del ScrolledText", command=mostrar_contenido)
boton.pack(pady=5)

etiqueta_resultado = tk.Label(ventana, text="", fg="blue", justify="left")
etiqueta_resultado.pack()

ventana.mainloop()
