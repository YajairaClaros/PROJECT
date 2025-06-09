# 6 - Controles de posición
import tkinter as tk

ventana = tk.Tk()
ventana.title("Controles de posición")
ventana.geometry("400x400")

# INTRODUCCIÓN:
# En Tkinter, existen tres métodos principales para posicionar widgets:
# 1. pack(): Posiciona automáticamente (superior/inferior/izquierda/derecha)
# 2. grid(): Usa filas y columnas (como una tabla)
# 3. place(): Usa coordenadas exactas (x, y)

# ----------------- pack() --------------------
# pack organiza los widgets uno debajo del otro por defecto

frame_pack = tk.LabelFrame(ventana, text="pack()", padx=10, pady=10)
frame_pack.pack(pady=10)

btn1 = tk.Button(frame_pack, text="Arriba")
btn2 = tk.Button(frame_pack, text="Abajo")
btn1.pack(side="top")
btn2.pack(side="bottom")


# ----------------- grid() --------------------
# grid organiza los widgets en filas y columnas (como una tabla)

frame_grid = tk.LabelFrame(ventana, text="grid()", padx=10, pady=10)
frame_grid.pack(pady=10)

lbl1 = tk.Label(frame_grid, text="Fila 0, Col 0", bg="lightblue")
lbl2 = tk.Label(frame_grid, text="Fila 0, Col 1", bg="lightgreen")
lbl3 = tk.Label(frame_grid, text="Fila 1, Col 0", bg="lightyellow")
lbl4 = tk.Label(frame_grid, text="Fila 1, Col 1", bg="lightpink")

lbl1.grid(row=0, column=0, padx=5, pady=5)
lbl2.grid(row=0, column=1, padx=5, pady=5)
lbl3.grid(row=1, column=0, padx=5, pady=5)
lbl4.grid(row=1, column=1, padx=5, pady=5)


# ----------------- place() --------------------
# place permite ubicar los widgets con coordenadas exactas

frame_place = tk.LabelFrame(ventana, text="place()", width=200, height=100)
frame_place.pack(pady=10)

# Usamos place para ubicar con coordenadas x, y dentro del frame
btn_place1 = tk.Button(frame_place, text="Botón A")
btn_place2 = tk.Button(frame_place, text="Botón B")
btn_place1.place(x=10, y=10)
btn_place2.place(x=100, y=40)

ventana.mainloop()
