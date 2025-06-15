import tkinter as tk



class Menu_Student(tk.Tk):
    
    def __init__(self, master=None, user=None):
        super().__init__(master)
        self.geometry("800x700")  # Dimensiones
        self.title("Menú estudiante")  # Título
        self.resizable(0, 0)  # Para que no se pueda modificar tamaño
        self.iconbitmap("Resources/Icons/logo_sin_letra_key.ico")
        self.configure(bg="white")  # color de fondo


        self.mainloop()

if __name__ == "__main__":
    app = Menu_Student()
    app.mainloop()

