import tkinter as tk
from Student.Menu import Menu_Student
from Admin.Menu import Menu_Admin
import Functions.Funciones as fun

class Login(tk.Tk):
    def __init__(self, master=None): #está definiendo el constructor de la clase. Es el metodo que se ejecuta automáticamente cuando creás un objeto de esa clase.
        super().__init__(master)# llama al constructor de la clase padre (tk.Tk()) para que se inicialice correctamente.
        self.geometry("600x400")
        self.title("Login")
        self.resizable(0, 0)
        self.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
        self.configure(bg="white")


        self.logo = tk.PhotoImage(file="Resources/Img/logo_key.png")

        tk.Label(self, text="Evaluación de clases", font=("Bookish", 20, "bold"), bg="white").pack()
        tk.Label(self, image=self.logo, bg="white").pack(pady=15)

        frame_login = tk.Frame(self, bg="white")
        frame_login.pack(pady=(40, 0))

        tk.Label(frame_login, text="Usuario:", font=("Bookish", 14), bg="white").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.entry_user = tk.Entry(frame_login, font=("Bookish", 14), width=25)
        self.entry_user.grid(row=0, column=1)

        tk.Label(frame_login, text="Contraseña:", font=("Bookish", 14), bg="white").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_contra = tk.Entry(frame_login, font=("Bookish", 14), width=25, show="*")
        self.entry_contra.grid(row=1, column=1)

        boton_login = tk.Button(frame_login, text="Iniciar sesión", font=("Simple", 12), width=15, height=2,
                                bg="black", fg="white", borderwidth=0, command=self.login)
        boton_login.grid(row=2, column=1, pady=(20, 0), padx=(0, 120))

        self.etiqueta_conf = tk.Label(self, text="", font=("Bookish", 14), bg="white")
        self.etiqueta_conf.pack()

    def login(self):
        user = self.entry_user.get()
        contra = self.entry_contra.get()

        if fun.login(user, contra):
            if fun.es_admin(user):
                self.abrir_menu_admin()
            else:
                self.abrir_menu_student()
        else:
            self.etiqueta_conf.configure(text="¡Usuario o contraseña incorrecta!")


    def abrir_menu_admin(self):
        user = self.entry_user.get()  # Guardás antes de destruir
        self.destroy()
        Menu_Admin(user=user)  # Luego los pasás

    def abrir_menu_student(self):

        user = self.entry_user.get()  # Guardás antes de destruir
        self.destroy()
        Menu_Student(user=user)  # Luego los pasás
if __name__ == "__main__":
    app = Login()
    app.mainloop()