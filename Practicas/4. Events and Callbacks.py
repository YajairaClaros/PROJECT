# 4 - Uso de events y callbacks
import tkinter as tk

# --------------------------------- Datos importantes antes de continuar ----------------------------------------
'''
| Atributo        | Descripción                                           |
| --------------- | ----------------------------------------------------- |
| `event.char`    | La letra o símbolo presionado (ej. "a", "5")          |
| `event.keysym`  | Nombre simbólico de la tecla (ej. "Return", "Escape")|
| `event.keycode` | Código numérico de la tecla                           |
| `event.x`       | Coordenada en x (del mouse)                           |
| `event.y`       | Coordenada en y (del mouse)                           |
| `event.widget`  | El widget donde ocurrió el evento                     |


| Evento              | Significado                         |
| ------------------- | ----------------------------------- |
| `<Key>`             | Cualquier tecla presionada          |
| `<KeyPress>`        | Presionar y mantener una tecla      |
| `<Return>`          | Enter                               |
| `<Escape>`          | Tecla ESC                           |
| `<BackSpace>`       | Borrar                              |
| `<Control-c>`       | Ctrl + C                            |


| Evento              | Significado                         |
| ------------------- | ----------------------------------- |
| `<Button-1>`        | Click izquierdo del mouse           |
| `<Button-2>`        | Click del botón central (rueda)     |
| `<Button-3>`        | Click derecho del mouse             |
| `<Double-Button-1>` | Doble clic izquierdo                |
| `<Motion>`          | Movimiento del mouse                |
| `<Enter>`           | Mouse entra al widget               |
| `<Leave>`           | Mouse sale del widget               |
| `<MouseWheel>`      | Rueda del mouse                     |
'''

ventana = tk.Tk()
ventana.title("Eventos y Callbacks")
ventana.geometry("500x400")

etiqueta = tk.Label(ventana, text="Interacción en tiempo real")
etiqueta.pack(pady=20)


# ---------------- Evento de teclado -------------------------
def tecla_presionada(event):
    etiqueta.config(text=f"Tecla presionada: {event.char}")

ventana.bind("<Key>", tecla_presionada)


# ---------------- Evento de teclas específicas ----------------
def enter_presionado(event):
    etiqueta.config(text="¡Presionaste ENTER!")

def escape_presionado(event):
    etiqueta.config(text="¡Saliste con ESC!")

ventana.bind("<Return>", enter_presionado)
ventana.bind("<Escape>", escape_presionado)


# ---------------- Click izquierdo ----------------------------
def click_izquierdo(event):
    etiqueta.config(text=f"Click izquierdo en ({event.x}, {event.y})")

ventana.bind("<Button-1>", click_izquierdo)


# ---------------- Click derecho ------------------------------
def click_derecho(event):
    etiqueta.config(text="Click derecho del mouse")

ventana.bind("<Button-3>", click_derecho)


# ---------------- Doble click izquierdo -----------------------
def doble_click(event):
    etiqueta.config(text="Doble clic detectado")

ventana.bind("<Double-Button-1>", doble_click)


# ---------------- Movimiento del mouse ------------------------
def movimiento_mouse(event):
    etiqueta.config(text=f"Mouse en ({event.x}, {event.y})")

ventana.bind("<Motion>", movimiento_mouse)


# ---------------- Mouse entra/sale de la ventana ---------------
def entra_mouse(event):
    etiqueta.config(text="El mouse entró a la ventana")

def sale_mouse(event):
    etiqueta.config(text="El mouse salió de la ventana")

ventana.bind("<Enter>", entra_mouse)
ventana.bind("<Leave>", sale_mouse)


# ---------------- Rueda del mouse -----------------------------
def rueda_mouse(event):
    etiqueta.config(text="Usaste la rueda del mouse")

ventana.bind("<MouseWheel>", rueda_mouse)


# --------------- Evento en un botón (callback directo) ----------
def al_hacer_click():
    etiqueta.config(text="¡Hiciste clic en el botón!")

boton = tk.Button(ventana, text="Haz clic aquí", command=al_hacer_click)
boton.pack(pady=10)

ventana.mainloop()
