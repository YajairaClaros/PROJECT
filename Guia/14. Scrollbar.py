#14 - Barras de desplazamiento (Scrollbar)
import tkinter as tk

ventana = tk.Tk()
ventana.title("Barras de desplazamiento")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# El widget Scrollbar permite añadir desplazamiento vertical u horizontal a otros widgets
# como Text, Canvas o Listbox cuando su contenido es mayor al tamaño visible.
# Debe vincularse al widget que se quiere desplazar.

# ------------------ Crear widget Text con Scrollbar ------------------

# Frame para agrupar ambos widgets
frame = tk.Frame(ventana)
frame.pack(pady=20, fill="both", expand=True)

# Widget de texto que contendrá mucho contenido
caja_texto = tk.Text(frame, wrap="word")  # wrap=word evita cortar palabras al final de línea
caja_texto.pack(side="left", fill="both", expand=True)

# Scrollbar vertical
scroll_vertical = tk.Scrollbar(frame, orient="vertical", command=caja_texto.yview)#Desp. Vertical
scroll_vertical.pack(side="right", fill="y")

# Vinculamos el scroll con el widget Text
caja_texto.config(yscrollcommand=scroll_vertical.set)

# ------------------ Insertar texto largo ------------------

for i in range(100):
    caja_texto.insert(tk.END, f"Línea {i+1}: Este es un ejemplo de texto con scroll.\n")

ventana.mainloop()
