#15 - Manejo de archivos (abrir y cerrar archivos)
import tkinter as tk
from tkinter import filedialog

ventana = tk.Tk()
ventana.title("Manejo de archivos")
ventana.geometry("600x400")

# INTRODUCCIÓN:
# En Tkinter se puede trabajar con archivos externos (como .txt) para leer o guardar información.
# Para esto se utiliza el módulo `filedialog`, que permite abrir ventanas del sistema
# para seleccionar archivos y rutas fácilmente.

# ------------------- Caja de texto para mostrar contenido -------------------

caja_texto = tk.Text(ventana, wrap="word")
caja_texto.pack(expand=True, fill="both", padx=10, pady=10)

# ------------------- Función para abrir un archivo -------------------

def abrir_archivo():
    ruta = filedialog.askopenfilename(
        title="Abrir archivo",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if ruta:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            caja_texto.delete("1.0", tk.END)  # Limpiamos la caja
            caja_texto.insert(tk.END, contenido)

# ------------------- Función para guardar un archivo -------------------

def guardar_archivo():
    ruta = filedialog.asksaveasfilename(
        title="Guardar archivo",
        defaultextension=".txt",
        filetypes=[("Archivos de texto", "*.txt")]
    )
    if ruta:
        with open(ruta, "w", encoding="utf-8") as archivo:
            contenido = caja_texto.get("1.0", tk.END)
            archivo.write(contenido)

# ------------------- Botones -------------------

frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)

boton_abrir = tk.Button(frame_botones, text="Abrir archivo", command=abrir_archivo)
boton_abrir.pack(side="left", padx=5)

boton_guardar = tk.Button(frame_botones, text="Guardar archivo", command=guardar_archivo)
boton_guardar.pack(side="left", padx=5)

ventana.mainloop()
