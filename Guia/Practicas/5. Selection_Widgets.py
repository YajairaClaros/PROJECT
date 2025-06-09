# 5 - Widgets de selección en Tkinter
import tkinter as tk

ventana = tk.Tk()
ventana.title("Widgets de selección")
ventana.geometry("400x400")

# INTRODUCCIÓN:
# Los widgets de selección son componentes gráficos que permiten al usuario
# elegir una o varias opciones dentro de una interfaz. Son muy comunes en
# formularios o menús interactivos.

# ------------------ Radiobutton ---------------------------
# Permite elegir UNA sola opción dentro de un grupo

# Variable de control asociada (de tipo entera, ya que value será un número),
# también hay para strings, doubles, booleans, etc
variable_raddio = tk.IntVar()

def mostrar_opcion():
    seleccion = variable_raddio.get()  # Obtiene el valor del radiobutton seleccionado
    resultado.config(text=f"Opción seleccionada: {seleccion}")

# Radiobuttons con variable asociada y valores únicos
#en variable colocamos la variable donde guardaremos la seleecion del resultado en este caso es variable_raddio
opcion1 = tk.Radiobutton(ventana, text="Opción 1", variable=variable_raddio, value=1, command=mostrar_opcion)
opcion2 = tk.Radiobutton(ventana, text="Opción 2", variable=variable_raddio, value=2, command=mostrar_opcion)
opcion3 = tk.Radiobutton(ventana, text="Opción 3", variable=variable_raddio, value=3, command=mostrar_opcion)

opcion1.pack()
opcion2.pack()
opcion3.pack()

resultado = tk.Label(ventana, text="Selecciona una opción")
resultado.pack(pady=10)


# ------------------ Checkbutton ----------------------------
# Permite seleccionar VARIAS opciones independientes (en términos de config es casi igual que los RadioButton)

# Cada checkbox debe tener su propia variable de control (tipo IntVar)
chk1_var = tk.IntVar()
chk2_var = tk.IntVar()

def mostrar_check():
    seleccionados = []
    if chk1_var.get() == 1:
        seleccionados.append("Check 1")
    if chk2_var.get() == 1:
        seleccionados.append("Check 2")
    texto = ", ".join(seleccionados) if seleccionados else "Ninguno"
    resultado_check.config(text=f"Seleccionados: {texto}")

check1 = tk.Checkbutton(ventana, text="Check 1", variable=chk1_var, command=mostrar_check)
check2 = tk.Checkbutton(ventana, text="Check 2", variable=chk2_var, command=mostrar_check)

check1.pack(pady=10)
check2.pack()

resultado_check = tk.Label(ventana, text="Selecciona uno o más checks")
resultado_check.pack(pady=10)

ventana.mainloop()
