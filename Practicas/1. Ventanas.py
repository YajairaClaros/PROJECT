# 1 - Uso de ventanas (Demosraciónde como funciona tkinter)
import tkinter as tk

#INTRODUCCIÓN: Una ventana es el contenedor principal de la aplicación gráfica.
# Es el espacio que aparece en pantalla cuando se ejecuta una app de Tkinter.
# Se crea con la clase Tk() y contiene todos los widgets (botones, etiquetas, cuadros de texto, etc.).

ventana = tk.Tk()
ventana.title("Suma de dos números")#Titulo
ventana.geometry("600x400")#Tamaño de pantalla
ventana.minsize(500, 200)#Tamaño mínimo de pantalla
ventana.maxsize(800, 500)#Tamaño máximo
ventana.iconbitmap("manzana.ico")#Icono de la app
#ventana.resizable(False, False)#Evita modificar el tamaño de la ventana

#Ventana para aplicar configuraciones como color de fondo, cursos y bordes
ventana.config(
    bg="white",         # Color de fondo
    cursor="hand2",     # Cursor del mouse
    relief="solid",    # Borde (opcional)
    bd=2             # Grosor del borde
)

ventana.config(bg="white")#Lo mismo que el anterior pero más abreviado

ventana.attributes("-alpha", 0.8)#transparencia de la ventana

#Comando para evitar que la ventana se cierre al instante
ventana.mainloop()