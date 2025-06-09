#13 - Widget de lienzo
import tkinter as tk

ventana = tk.Tk()
ventana.title("Widget de Lienzo")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# El widget Canvas permite dibujar figuras geométricas, mostrar imágenes, crear gráficos y animaciones.
# Es ideal para interfaces más gráficas o interactivas donde se necesita control sobre cada elemento visual.

# ------------------------ Crear lienzo ------------------------

lienzo = tk.Canvas(ventana, width=500, height=300, bg="white")
lienzo.pack(pady=20)

# ------------------------ Dibujar figuras ------------------------

# Línea: coordenadas x1, y1, x2, y2
lienzo.create_line(50, 50, 200, 50, fill="red", width=2)

# Rectángulo: coordenadas x1, y1, x2, y2
lienzo.create_rectangle(50, 100, 200, 180, fill="lightblue", outline="blue")

# Óvalo (círculo o elipse dentro del rectángulo dado)
lienzo.create_oval(250, 100, 350, 180, fill="green")

# Texto
lienzo.create_text(250, 50, text="¡Holaaaaaaaaaaa!", font=("Arial", 14), fill="purple")

# ------------------------ Ejemplo dinámico ------------------------

def mover_circulo():
    # Mueve el óvalo 10px a la derecha y 0 hacia abajo
    lienzo.move(circulo_id, 10, 0)

# Crear otro óvalo y moverlo al hacer clic en botón
circulo_id = lienzo.create_oval(100, 220, 140, 260, fill="orange")

boton = tk.Button(ventana, text="Mover círculo", command=mover_circulo)
boton.pack()

ventana.mainloop()
