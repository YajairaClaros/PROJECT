import tkinter as tk




class Menu_Student(tk.Tk):
    
    def __init__(self, master=None, user=None):
        super().__init__(master)
        try:
            with open("../Usuario_Logueado.txt", "r") as f:
                user = f.read().strip()
        except:
            with open("Usuario_Logueado.txt", "r") as f:
                user = f.read().strip()

        try:
            self.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
        except:
            self.iconbitmap("../Resources/Icons/logo_sin_letra_key.ico")

        self.geometry("700x500")  # Dimensiones
        self.title("Menú estudiante")  # Título
        self.resizable(0, 0)  # Para que no se pueda modificar tamaño
        self.configure(bg="white")  # color de fondo

        try:
            self.logo = tk.PhotoImage(file="Resources/Img/logo_key.png")
        except:
            self.logo = tk.PhotoImage(file="../Resources/Img/logo_key.png")


        self.label_logo = tk.Label(self, image=self.logo, bg="white")
        self.label_logo.grid(column=0, row=0)

        tk.Label(self, text=f"¡Bienvenido {user}!", font=("Bookish", 18), bg="white").grid(row=1,
                                                                                                         column=0,
                                                                                                         columnspan=2)

        # Asegúrate que el frame pueda expandirse

        self.grid_columnconfigure(1, weight=1)



if __name__ == "__main__":
    app = Menu_Student()
    app.mainloop()

