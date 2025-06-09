#12 - Gestor de imagenes (Photoimage)
import tkinter as tk

ventana = tk.Tk()
ventana.title("Gestor de imágenes")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# Tkinter permite mostrar imágenes mediante el gestor de imágenes llamado PhotoImage.
# Este widget funciona principalmente con imágenes en formato .gif o .png (no soporta JPG directamente).
# Las imágenes pueden colocarse en etiquetas, botones, etc.

# ------------------------ Cargar y mostrar imagen ------------------------

# Cargar imagen (debe ser formato .png o .gif y estar en la misma carpeta que el archivo .py)
imagen = tk.PhotoImage(file="ejemplo.png")  # Asegúrate que 'ejemplo.png' exista

# Mostrar la imagen en una etiqueta
etiqueta_imagen = tk.Label(ventana, image=imagen)
etiqueta_imagen.pack(pady=10)

# ------------------------ Imagen en un botón ------------------------

def accion_boton():
    etiqueta_resultado.config(text="¡Has hecho clic en el botón con imagen!")

# Usamos la misma imagen para un botón
boton_imagen = tk.Button(ventana, image=imagen, command=accion_boton)
boton_imagen.pack(pady=5)

# Etiqueta de resultado
etiqueta_resultado = tk.Label(ventana, text="", fg="green")
etiqueta_resultado.pack()

# IMPORTANTE: se debe mantener una referencia a la imagen
# Si no se guarda en una variable (como "imagen"), la imagen no se mostrará

ventana.mainloop()
