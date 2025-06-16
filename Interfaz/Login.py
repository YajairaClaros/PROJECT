import tkinter as tk
from tkinter import ttk #Widgets más modernosrr
from Interfaz.Student.Menu import Menu_Student
from Interfaz.Admin.Menu import Menu_Admin
import Interfaz.Functions.Funciones as fun

class Login(tk.Tk):
    def __init__(self, master=None):
        super().__init__(master)

        # Intento cargar ícono desde dos ubicaciones posibles
        try:
            self.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
        except:
            self.iconbitmap("../Resources/Icons/logo_sin_letra_key.ico")

        self.geometry("600x400")
        self.title("Login")
        self.resizable(0, 0)
        self.configure(bg="white")

        # Estilos personalizados con nombres descriptivos
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("Texto.TLabel", background="white", font=("Bookish", 14))
        style.configure("Titulo.TLabel", font=("Bookish", 20, "bold"), background="white")
        style.configure("Boton.TButton", font=("Simple", 12), padding=6)
        style.configure("BotonNegro.TButton", font=("Simple", 12), foreground="white", background="black", relief="flat")
        style.map("BotonNegro.TButton", background=[('active', '#333333')])  # Efecto hover
        style.configure("Entrada.TEntry", padding=5, font=("Bookish", 12))

        # Intento cargar el logo desde dos rutas posibles
        try:
            self.logo = tk.PhotoImage(file="Resources/Img/logo_key.png")
        except:
            self.logo = tk.PhotoImage(file="../Resources/Img/logo_key.png")

        ttk.Label(self, text="Evaluación de clases", style="Titulo.TLabel").pack()
        tk.Label(self, image=self.logo, bg="white").pack(pady=15)

        frame_login = ttk.Frame(self, style="Texto.TLabel")
        frame_login.pack(pady=(40, 0))

        ttk.Label(frame_login, text="Usuario:", style="Texto.TLabel").grid(row=0, column=0, sticky="e", padx=10, pady=10)
        self.entry_user = ttk.Entry(frame_login, width=25, style="Entrada.TEntry")
        self.entry_user.grid(row=0, column=1)

        ttk.Label(frame_login, text="Contraseña:", style="Texto.TLabel").grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.entry_contra = ttk.Entry(frame_login, width=25, show="*", style="Entrada.TEntry")
        self.entry_contra.grid(row=1, column=1)

        boton_login = ttk.Button(frame_login, text="Iniciar sesión", style="BotonNegro.TButton", command=self.login)
        boton_login.grid(row=2, column=1, pady=(20, 0), padx=(0, 120))

        self.etiqueta_conf = ttk.Label(self, text="", style="Texto.TLabel")
        self.etiqueta_conf.pack()

    def login(self):
        user = self.entry_user.get()
        contra = self.entry_contra.get()

        if fun.login(user, contra):
            # Guardar usuario logueado en archivo
            try:
                with open("../Usuario_Logueado.txt", "w") as f:
                    f.write(user)
            except:
                with open("Usuario_Logueado.txt", "w") as f:
                    f.write(user)

            # Redirigir al menú correspondiente
            if fun.es_admin(user):
                self.abrir_menu_admin()
            else:
                self.abrir_menu_student()
        else:
            self.etiqueta_conf.configure(text="¡Usuario o contraseña incorrecta!")

    def abrir_menu_admin(self):
        self.destroy()
        Menu_Admin()

    def abrir_menu_student(self):
        self.destroy()
        Menu_Student()

if __name__ == "__main__":
    app = Login()
    app.mainloop()
