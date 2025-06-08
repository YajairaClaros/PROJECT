# 3 - Uso de widgets básicos
import tkinter as tk
import time #Para usar tiempo


def update_time():#Esto muestra la hora actual
    etiquette.config(text=time.strftime("%H:%M:%S"))
    ventana.after(1000, update_time)


ventana = tk.Tk()

ventana.title("Widgets básicos")
ventana.geometry("500x300")


#---------------- Etiqueta ------------------------------
etiquette = tk.Label(ventana, text="Etiquetaaaaaa")
etiquette.config(bg="black", fg="white", padx=10, pady=10)
etiquette.pack()

update_time()


# ----------------- Botones -------------------------------
def saludar():
    etiquette.config(text="¡Hola! Presionaste el botón.")

# Botón simple que al presionar cambia el texto de la etiqueta
#NOTA: SE PONE VENTANA YA QUE ES DONDE IRÁ EL WIDGET, SI FUERA UN FRAME ENTONCES SE PONE EL NOMBRE DEL FRAME
boton_saludo = tk.Button(ventana, text="Saludar", command=saludar) #Agregamos command para la función que queremos ejecutar en este caso es "saludar()"
boton_saludo.config(bg="green", fg="white", padx=10, pady=5)
boton_saludo.pack(pady=5)

# Botón para cerrar la ventana
boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
boton_salir.config(bg="red", fg="white", padx=10, pady=5)
boton_salir.pack(pady=5)



# ---------------------- Entrys -----------------------------
def mostrar_texto():
    texto = entrada.get() #Usamos get para tomar el dato que esta ingresando el usuario en este caso esta en la var "entrada"
    etiquette.config(text=f"Escribiste: {texto}") #En la etiqueta mostramos lo que ingreso

entrada = tk.Entry(ventana)
entrada.pack(pady=5)

boton_mostrar = tk.Button(ventana, text="Mostrar texto", command=mostrar_texto)
boton_mostrar.pack(pady=5)




ventana.mainloop()