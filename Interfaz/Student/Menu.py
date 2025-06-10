import tkinter as tk


def abrir_menu():
    ventana = tk.Tk()
    ventana.geometry("600x400")  # Dimensiones
    ventana.title("Menú")  # Título
    ventana.resizable(0, 0)  # Para que no se pueda modificar tamaño
    ventana.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
    ventana.configure(bg="white")  # color de fondo
    ventana.mainloop()
