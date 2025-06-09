#9 - Widgets de menú (Menubutton, Menu y menús contextuales
import tkinter as tk

ventana = tk.Tk()
ventana.title("Widgets de Menú")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# Tkinter permite crear menús para ofrecer opciones al usuario:
# - Menu: barra de menú tradicional (como Archivo, Edición)
# - Menubutton: botón con menú desplegable
# - Menús contextuales: aparecen al hacer clic derecho

# ------------------------ Menú principal (barra superior) ------------------------

def accion_archivo():
    etiqueta.config(text="Elegiste una opción del menú Archivo")

def accion_edicion():
    etiqueta.config(text="Elegiste una opción del menú Edición")

# Creamos la barra de menú
menu_barra = tk.Menu(ventana)
ventana.config(menu=menu_barra)  # Se asigna como menú principal de la ventana

# Creamos el submenú "Archivo"
menu_archivo = tk.Menu(menu_barra, tearoff=0)  # tearoff=0 evita que se pueda "separar" el menú
menu_archivo.add_command(label="Nuevo", command=accion_archivo)  # Opción del menú
menu_archivo.add_command(label="Abrir", command=accion_archivo)
menu_archivo.add_separator()  # Línea separadora
menu_archivo.add_command(label="Salir", command=ventana.quit)  # Sale de la app

# Creamos el submenú "Edición"
menu_edicion = tk.Menu(menu_barra, tearoff=0)
menu_edicion.add_command(label="Copiar", command=accion_edicion)
menu_edicion.add_command(label="Pegar", command=accion_edicion)

# Agregamos los submenús a la barra
menu_barra.add_cascade(label="Archivo", menu=menu_archivo)
menu_barra.add_cascade(label="Edición", menu=menu_edicion)

# ------------------------ Menubutton ------------------------

def opcion_elegida():
    etiqueta.config(text="Seleccionaste una opción del Menubutton")

# Menubutton es un botón que al hacer clic despliega un menú
menu_btn = tk.Menubutton(ventana, text="Opciones", relief="raised")  # relief es el estilo del borde
menu_btn.menu = tk.Menu(menu_btn, tearoff=0)  # Creamos el menú para el Menubutton
menu_btn["menu"] = menu_btn.menu  # Asociamos el menú al botón

# Agregamos opciones al menú del Menubutton
menu_btn.menu.add_command(label="Opción 1", command=opcion_elegida)
menu_btn.menu.add_command(label="Opción 2", command=opcion_elegida)

menu_btn.pack(pady=10)  # Mostramos el Menubutton

# ------------------------ Menú contextual (clic derecho) ------------------------

def mostrar_menu_contextual(event):
    # post(x, y) muestra el menú en la posición del puntero
    menu_contextual.post(event.x_root, event.y_root)  # Coordenadas globales del mouse

def opcion_contextual():
    etiqueta.config(text="Menú contextual activado")

# Creamos el menú contextual (como el que aparece al hacer clic derecho)
menu_contextual = tk.Menu(ventana, tearoff=0)
menu_contextual.add_command(label="Opción contextual", command=opcion_contextual)

# Asociamos el evento del clic derecho a la ventana principal
ventana.bind("<Button-3>", mostrar_menu_contextual)  # Button-3 = clic derecho del mouse

# ------------------------ Etiqueta de salida ------------------------

etiqueta = tk.Label(ventana, text="Interacción con menús")
etiqueta.pack(pady=20)

ventana.mainloop()

