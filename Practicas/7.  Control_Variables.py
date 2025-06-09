#7 - Variables de control (stringvar, intvar, doublevar, booleanvar) y uso del SpinBox
import tkinter as tk

ventana = tk.Tk()
ventana.title("Variables de control")
ventana.geometry("400x400")

# INTRODUCCIÓN:
# Las variables de control permiten almacenar y vincular datos entre los widgets y el programa.
# Se usan con widgets como Entry, Checkbutton, Radiobutton, etc.
# Tipos comunes:
# - StringVar: cadenas de texto
# - IntVar: números enteros
# - DoubleVar: números decimales
# - BooleanVar: valores True o False

# ------------------ StringVar --------------------
texto_var = tk.StringVar()
texto_var.set("Texto inicial")

def actualizar_texto():
    resultado.config(text=f"Texto ingresado: {texto_var.get()}")

entrada = tk.Entry(ventana, textvariable=texto_var)
entrada.pack(pady=5)

btn_texto = tk.Button(ventana, text="Mostrar texto", command=actualizar_texto)
btn_texto.pack()

resultado = tk.Label(ventana, text="")
resultado.pack(pady=10)


# ------------------ IntVar --------------------
#El Spinbox se usa para que el usuario ingrese únicamente números
numero_var = tk.IntVar()
numero_var.set(10)

def mostrar_numero():
    lbl_numero.config(text=f"Valor actual: {numero_var.get()}")

spin = tk.Spinbox(ventana, from_=0, to=100, textvariable=numero_var)
spin.pack(pady=5)

btn_num = tk.Button(ventana, text="Mostrar número", command=mostrar_numero)
btn_num.pack()

lbl_numero = tk.Label(ventana, text="")
lbl_numero.pack(pady=10)


# ------------------ BooleanVar --------------------
bool_var = tk.BooleanVar()
bool_var.set(False)

def mostrar_booleano():
    estado = "Activado" if bool_var.get() else "Desactivado"
    lbl_booleano.config(text=f"Estado: {estado}")

check = tk.Checkbutton(ventana, text="Activar opción", variable=bool_var, command=mostrar_booleano)
check.pack(pady=5)

lbl_booleano = tk.Label(ventana, text="")
lbl_booleano.pack(pady=10)

ventana.mainloop()
