import tkinter as tk


def sumar():
    try:
        num1 = float(entrada1.get())
        num2 = float(entrada2.get())
        suma = num1 + num2
        resultado.config(text=f"Resultado: {suma}")
    except ValueError:
        resultado.config(text="Por favor, ingresa números válidos.")

ventana = tk.Tk()
ventana.title("Suma de dos números")
ventana.geometry("700x400")


tk.Label(ventana, text="Número 1:").pack()
entrada1 = tk.Entry(ventana)
entrada1.pack()

tk.Label(ventana, text="Número 2:").pack()
entrada2 = tk.Entry(ventana)
entrada2.pack()

boton_sumar = tk.Button(ventana, text="Sumar")
boton_sumar.pack(padx=5, pady=5)

resultado = tk.Label(ventana, text="Resultado: ")
resultado.pack()

ventana.mainloop()
