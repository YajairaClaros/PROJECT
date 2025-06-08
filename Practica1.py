import tkinter as tk


def sumar():
    try:
        num1 = float(entrada1.get())
        num2 = float(entrada2.get())
        suma = num1 + num2
        resultado.config(text=f"Resultado: {suma}")
    except ValueError:
        resultado.config(text="Por favor, ingresa números válidos.")

ventana = tk.Tk()
ventana.title("Suma de dos números")#Titulo
ventana.geometry("600x400")#Tamaño de pantalla
ventana.minsize(500, 200)#Tamaño mínimo de pantalla
ventana.maxsize(800, 500)#Tamaño máximo
ventana.iconbitmap("manzana.ico")#Icono de la app


#Ventana para aplicar configuraciones como color de fondo, cursos y bordes
ventana.config(
    bg="white",         # Color de fondo
    cursor="hand2",     # Cursor del mouse
    relief="solid",    # Borde (opcional)
    bd=2             # Grosor del borde
)


ventana.config(bg="white")#Lo mismo que el anterior pero más abreviado

#Entrada de texto 1
tk.Label(ventana, text="Número 1:").pack()
entrada1 = tk.Entry(ventana)
entrada1.pack()

#Entrada de texto 2
tk.Label(ventana, text="Número 2:").pack()
entrada2 = tk.Entry(ventana)
entrada2.pack()

#Botón para sumar
boton_sumar = tk.Button(ventana, text="Sumar", command=sumar)
boton_sumar.pack(padx=5, pady=5)

#Etiqueta que muestra el resultado
resultado = tk.Label(ventana, text="Resultado: ")
resultado.pack()

#Comando para evitar que la ventana se cierre al instante
ventana.mainloop()
