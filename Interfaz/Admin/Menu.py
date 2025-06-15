import tkinter as tk
from tkinter import PhotoImage


class Menu_Admin(tk.Tk):

    def __init__(self,master=None,user=None):
        super().__init__(master)
        self.title("Menú Administrador")
        self.geometry("900x700")  # Dimensiones
        self.resizable(0, 0)  # Para que no se pueda modificar tamaño
        self.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
        self.configure(bg="white")  # color de fondo

#------------------------------------------------- Inicio del menú -----------------------------------------------
        # Estado del menú: expandido o contraído
        self.menu_expandido = True

        # Contenedor principal
        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.menu_frame = tk.Frame(self.container, bg="#8700ff", width=200)
        self.menu_frame.pack(side="left", fill="y")

        # Botón de contraer/expandir menú
        self.toggle_btn = tk.Button(self.menu_frame, text="≡", bg="#8700ff", fg="white",
                                    command=self.toggle_menu, borderwidth=0, font=("Bookish", 16, "bold"))
        self.toggle_btn.pack(pady=10)

        # Botones del menú
        self.icono_maestros = PhotoImage(file="Resources/Img/people.png")#El parámetro compound controla cómo se muestran el texto y la imagen juntos dentro del widge
        self.btn_inicio = tk.Button(self.menu_frame, text="Docentes", bg="#8700ff", fg="white", compound="left",
                                     anchor="w", padx=5, relief="flat", font=("Bookish", 14, "bold"), image=self.icono_maestros)
        self.btn_inicio.pack(fill="x", pady=5)

        self.icono_materias= PhotoImage(file="Resources/Img/asignature.png")
        self.btn_materias = tk.Button(self.menu_frame, text="Materias", bg="#8700ff", fg="white", compound="left",
                                       anchor="w", padx=5, relief="flat",
                                      font=("Bookish", 14, "bold"), image=self.icono_materias)
        self.btn_materias.pack(fill="x", pady=5)

        self.icono_estudiantes = PhotoImage(file="Resources/Img/student.png")
        self.btn_usuarios = tk.Button(self.menu_frame, text="Estudiantes", bg="#8700ff", fg="white", compound="left",
                                       anchor="w", padx=5, relief="flat", font=("Bookish", 14, "bold"), image=self.icono_estudiantes)
        self.btn_usuarios.pack(fill="x", pady=5)
# ----------------------------------------------- Final del Menú --------------------------------------------



#------------------------------------------------ Contenido --------------------------------------------------
        self.content_frame = tk.Frame(self.container, bg="white")

        self.logo = tk.PhotoImage(file="Resources/Img/logo_key.png")

        self.label_logo = tk.Label(self.content_frame, image=self.logo, bg="white")
        self.label_logo.grid(column=0, row=0)

        self.content_frame.pack(side="left", fill="both", expand=True)
        tk.Label(self.content_frame, text=f"¡Bienvenido {user}!", font=("Bookish", 18), bg="white").grid(row=1, column=0, columnspan=2)

        # Asegúrate que el frame pueda expandirse

        self.content_frame.grid_columnconfigure(1, weight=1)





    def toggle_menu(self):
        if self.menu_expandido:
            # Contraer menú
            self.menu_frame.config(width=75)
            self.btn_inicio.config(text="")
            self.btn_usuarios.config(text="")
            self.btn_materias.config(text="")
        else:
            # Expandir menú
            self.menu_frame.config(width=300)
            self.btn_inicio.config(text="Docentes")
            self.btn_usuarios.config(text="Estudiantes")
            self.btn_materias.config(text="Materias")
        self.menu_expandido = not self.menu_expandido #Invierte el bool
#------------------------------------------------ Fin del Contenido --------------------------------------------------

if __name__ == "__main__":
    app = Menu_Admin()
    app.mainloop()
