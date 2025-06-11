import tkinter as tk
from Student.Menu import abrir_menu as menu_student #Importamos la función que abre el menú de estudiante
from Admin.Menu import abrir_menu as menu_admin#Importamos la función que abre el menú de admin
import Functions.Funciones as fun

#Función para abrir el menú de admin
def abrir_menu_admin():
    # Cerrar ventana de login
    ventana.destroy()
    # Abir menú estudiante
    menu_admin()

#Función para abrir el menu estudiante
def abrir_menu_student():
    # Cerrar ventana de login
    ventana.destroy()
    # Abir menú estudiante
    menu_student()

#Función para verfificar si los datos del login son correctos (usuario y contraseña)
def login():
    user = entry_user.get()
    contra = entry_contra.get()

    #Llamamos a la función para verificar si el usuario y contraseña son correcto
    usuarios = fun.login(user, contra)
    if usuarios:
        esadmin = fun.es_admin(user)
        if esadmin:
            abrir_menu_admin()
        else:
            abrir_menu_student()


    else:
        etiqueta_conf.configure(text="¡Usuario y contraseña y incorrecta!")

ventana = tk.Tk()
ventana.geometry("600x400")#Dimensiones
ventana.title("Login")#Título
ventana.resizable(0, 0)#Para que no se pueda modificar tamaño
ventana.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
ventana.configure(bg="white")#color de fondo

#Código para colocar el logo
Logo = tk.PhotoImage(file="Resources/Img/logo_key.png")


etiqueta_user = tk.Label(ventana, text="Evaluación de clases")
etiqueta_user.config(font=("Bookish", 20, "bold"), bg="white")
etiqueta_user.pack()

etiqueta_logo = tk.Label(ventana, image=Logo)
etiqueta_logo.config(bg="white")
etiqueta_logo.pack(pady=15)

#Código para los campos de entrada
#Frame para el login y usamos grid para organizar mejor
frame_login = tk.Frame(ventana, width=200, height=200)
frame_login.config(bg="white")
frame_login.pack(pady=(40,0))

#Entrada del nombre
etiqueta_user = tk.Label(frame_login, text="Usuario: ", anchor="e")#sticky="e" y anchor="e" para alinear a la derecha
etiqueta_user.config(font=("Bookish", 14), padx=10, pady=10, bg="white")
etiqueta_user.grid(row=0, column=0, sticky="e")

entry_user = tk.Entry(frame_login, width=25, borderwidth=2)
entry_user.config(font=("Bookish", 14), borderwidth=2)
entry_user.grid(row=0, column=1)

#Entrada de la contra
etiqueta_contra = tk.Label(frame_login, text="Contraseña: ")
etiqueta_contra.config(font=("Bookish", 14), padx=10, pady=10, bg="white")
etiqueta_contra.grid(row=1, column=0)

entry_contra = tk.Entry(frame_login, width=25, borderwidth=2, show="*")
entry_contra.config(font=("Bookish", 14), borderwidth=2)
entry_contra.grid(row=1, column=1)


#Botones

boton_login = tk.Button(frame_login, text="Iniciar sesión",width=15, height=2, bg="black", borderwidth=0, command=login)
boton_login.config(font=("Simple", 12),  fg="white")
boton_login.grid(row=2, column=1, padx=(0,120),pady=(20,0))


#Etiqueta para confirmar inicio de sesion
etiqueta_conf = tk.Label(ventana, text="", font=("Bookish", 14))
etiqueta_conf.pack()


ventana.mainloop()