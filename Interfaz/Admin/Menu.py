import tkinter as tk
from tkinter import ttk

from Interfaz.Admin.Estudiantes import Ver_Estudiantes
from Interfaz.Admin.Maestros import Ver_Maestros
from Interfaz.Admin.Inicio import Ver_Inicio
from Interfaz.Admin.Materias import Ver_Materias


class Menu_Admin(tk.Tk):

    def __init__(self, master=None):
        super().__init__(master)

        #Acá cargamos el logo que aparece en la esquina de la ventana
        try:
            self.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
        except:
            self.iconbitmap("../Resources/Icons/logo_sin_letra_key.ico")

        self.withdraw()  # Ocultamos mientras configuramos
        self.title("Administrador")
        self.geometry("800x600")
        self.state("zoomed")#Para que inicie en pantalla completa
        self.minsize(800, 600)
        self.configure(bg="white")

        # Estilos ttk
        style = ttk.Style(self)

        # Usar tema que respeta colores personalizados
        style.theme_use("clam")

        style.configure("TLabel", background="white", font=("Bookish", 12))
        style.configure("TButton", font=("Bookish", 12))
        style.configure("Treeview", font=("Bookish", 11))
        style.configure("Treeview.Heading", font=("Bookish", 12, "bold"))
        style.configure("White.TFrame", background="white")

        # Estilo personalizado para botón negro con texto blanco
        style.configure("Black.TButton",
                        background="black", foreground="white",
                        borderwidth=1, focusthickness=3, focuscolor='none', relief='flat')
        style.map("Black.TButton",
                  background=[("active", "#333333"), ("!disabled", "black")],
                  foreground=[("active", "white"), ("!disabled", "white")])
        # Estilo del encabezado de la tabla
        style.configure("Treeview.Heading",
                        font=("Bookish", 12, "bold"),
                        background="#8700ff",  # color de fondo del encabezado
                        foreground="white",  # color del texto del encabezado
                        relief="flat")  # apariencia 3D opcional

        # --------------------- Menú lateral (tk para conservar colores) ---------------------
        self.menu_expandido = True

        self.container = ttk.Frame(self, style="White.TFrame")
        self.container.pack(fill="both", expand=True)

        self.menu_frame = tk.Frame(self.container, bg="#8700ff", width=200)
        self.menu_frame.pack(side="left", fill="y")

        self.toggle_btn = tk.Button(self.menu_frame, text="≡", bg="#8700ff", fg="white",
                                    command=self.toggle_menu, borderwidth=0, font=("Bookish", 16, "bold"))
        self.toggle_btn.pack(pady=10)

        # -----------------------Botón para abrir incio
        try:
            self.icono_inicio = tk.PhotoImage(file="Resources/Img/house.png")
        except:
            self.icono_inicio = tk.PhotoImage(file="../Resources/Img/house.png")

        self.btn_inicio = tk.Button(self.menu_frame, text="Inicio", bg="#8700ff", fg="white", compound="left", command=lambda: self.cambiar_vista(
            1),
                                    anchor="w", padx=5, relief="flat", font=("Bookish", 14, "bold"),
                                    image=self.icono_inicio)
        self.btn_inicio.pack(fill="x", pady=5)

        #-----------------------Botón para abrir maestros
        try:
            self.icono_maestros = tk.PhotoImage(file="Resources/Img/people.png")
        except:
            self.icono_maestros = tk.PhotoImage(file="../Resources/Img/people.png")

        self.btn_maestros = tk.Button(self.menu_frame, text="Maestros", bg="#8700ff", fg="white", compound="left", command=lambda: self.cambiar_vista(2),  #crea una función anónima que, cuando se llama, ejecuta self.cambiar(1). Así la función solo se ejecutará cuando el botón sea presionado.
                                      anchor="w", padx=5, relief="flat", font=("Bookish", 14, "bold"), image=self.icono_maestros)
        self.btn_maestros.pack(fill="x", pady=5)

        # -----------------------Botón para abrir materias
        try:
            self.icono_materias = tk.PhotoImage(file="Resources/Img/asignature.png")
        except:
            self.icono_materias = tk.PhotoImage(file="../Resources/Img/asignature.png")

        self.btn_materias = tk.Button(self.menu_frame, text="Materias", bg="#8700ff", fg="white", compound="left", command=lambda: self.cambiar_vista(3),
                                      anchor="w", padx=5, relief="flat", font=("Bookish", 14, "bold"), image=self.icono_materias)
        self.btn_materias.pack(fill="x", pady=5)

        # -----------------------Botón para abrir estudiantes
        try:
            self.icono_estudiantes = tk.PhotoImage(file="Resources/Img/student.png")
        except:
            self.icono_estudiantes = tk.PhotoImage(file="../Resources/Img/student.png")

        self.btn_usuarios = tk.Button(self.menu_frame, text="Estudiantes", bg="#8700ff", fg="white", compound="left", command=lambda: self.cambiar_vista(4),
                                      anchor="w", padx=5, relief="flat", font=("Bookish", 14, "bold"), image=self.icono_estudiantes)
        self.btn_usuarios.pack(fill="x", pady=5)


        # ---------------------- Contenido principal (ttk con fondo blanco) ----------------------
        self.content_frame = ttk.Frame(self.container, style="White.TFrame")
        self.content_frame.pack(side="left", fill="both", expand=True)
        #Abrimos cada ventana dependiendo la opcion


        self.update_idletasks()  # Procesar tod antes de mostrar
        self.deiconify()  # Mostrar ventana sin parpadeo
        self.focus()  # Poner foco en la ventana secundaria

        #Que se muestre el logo
        try:
            self.logo = tk.PhotoImage(file="Resources/Img/logo_key.png")
        except:
            self.logo = tk.PhotoImage(file="../Resources/Img/logo_key.png")

        self.label_logo = ttk.Label(self.content_frame, image=self.logo, style="White.TLabel")
        self.label_logo.grid(column=0, row=0, sticky="nw")

        self.Ver_Inicio()

    def toggle_menu(self):
        if self.menu_expandido:
            self.menu_frame.config(width=75)
            self.btn_maestros.config(text="")
            self.btn_usuarios.config(text="")
            self.btn_materias.config(text="")
            self.btn_inicio.config(text="")
        else:
            self.menu_frame.config(width=300)
            self.btn_inicio.config(text="Inicio")
            self.btn_maestros.config(text="Maestros")
            self.btn_usuarios.config(text="Estudiantes")
            self.btn_materias.config(text="Materias")
        self.menu_expandido = not self.menu_expandido

    def cambiar_vista(self,opcion):
        for widget in self.content_frame.winfo_children():#cuando quieres obtener una lista de todos los widgets hijos (widgets contenidos) dentro de un contenedor
            if widget != self.label_logo:#Para q no elimine el logo
                widget.destroy()

        if opcion == 1:
          self.Ver_Inicio()
        elif opcion == 2:
          self.Ver_Maestros()
        elif opcion == 3:
          self.Ver_Materias()
        elif opcion == 4:
            self.Ver_Estudiantes()

    #Esta función llama a Inicio
    def Ver_Inicio(self):
        # Usamos el módulo de Inicio
        opcion_inicio = Ver_Inicio(self.content_frame)
        opcion_inicio.mostrar()

    def Ver_Maestros(self):
        # Usamos el módulo de Maestros
        opcion_maestros = Ver_Maestros(self.content_frame)
        opcion_maestros.mostrar()

    def Ver_Materias(self):
        # Usamos el módulo de Maestros
        opcion_materias = Ver_Materias(self.content_frame)
        opcion_materias.mostrar()

    def Ver_Estudiantes(self):
        opcion_estudiantes = Ver_Estudiantes(self.content_frame)
        opcion_estudiantes.mostrar()

if __name__ == "__main__":
    app = Menu_Admin()
    app.mainloop()
