# 2 - uso de Frames
import tkinter as tk

ventana = tk.Tk()

ventana.title("Titulo de mi ventana")
ventana.geometry("600x400")#Tamaño de pantalla
ventana.configure(bg="blue")


#--------------Los frames son contenedores a los cuales les podemos agregar cosas-----------
frame1 = tk.Frame(ventana)
frame1.configure(width=300, height=200, bg="red", bd=5)#Se configura igual que la ventana

#Podemos meter frames dentro de otro colocando dentro de Frame() el nombre del frame, en este caso lo metemos a frame 1
frame2 = tk.Frame(frame1)
frame2.configure(width=100, height=100, bg="green", bd=5)

frame1.pack()
frame2.pack()

boton = tk.Button(frame1, text="Holaaaaaaaaaaa")
boton.pack()


# -------------------- Un label frame es un frame pero con título ---------------
labelframe = tk.LabelFrame(ventana, text="Grupo de objetos", width=300, height=100, bg="yellow")
labelframe.configure(width=300, height=100)
labelframe.pack()

#Comando para evitar que la ventana se cierre al instante
ventana.mainloop()