# 4 - Uso de events y callbacks
import tkinter as tk

# --------------------------------- Datos importantes antes de continuar ----------------------------------------
'''
# --------- EVENTOS DE TECLADO ----------
# Se disparan cuando se presionan o sueltan teclas

"<Key>"             # Cualquier tecla presionada
"<KeyPress>"        # Igual que <Key>
"<KeyRelease>"      # Cuando se suelta una tecla

"<Return>"          # Enter
"<Escape>"          # ESC
"<BackSpace>"       # Retroceso
"<Tab>"             # TAB
"<space>"           # Espacio
"<Delete>"          # Tecla DELETE

"<Up>"              # Flecha arriba
"<Down>"            # Flecha abajo
"<Left>"            # Flecha izquierda
"<Right>"           # Flecha derecha

"<Shift_L>"         # Shift izquierdo
"<Control_L>"       # Ctrl izquierdo
"<Alt_L>"           # Alt izquierdo

"<Control-KeyPress-a>"  # Ctrl + A (combinación personalizada)


# --------- EVENTOS DE MOUSE ----------
# Se disparan con clics, movimientos o scroll del mouse

"<Button-1>"        # Clic izquierdo
"<Button-2>"        # Clic central (rueda)
"<Button-3>"        # Clic derecho

"<Double-Button-1>" # Doble clic izquierdo
"<Triple-Button-1>" # Triple clic izquierdo
"<ButtonRelease-1>" # Cuando se suelta el botón izquierdo

"<Motion>"          # Movimiento del mouse
"<Enter>"           # Mouse entra al widget
"<Leave>"           # Mouse sale del widget

"<MouseWheel>"      # Scroll de la rueda del mouse (Windows/macOS)
"<Button-4>"        # Scroll arriba (Linux)
"<Button-5>"        # Scroll abajo (Linux)


# --------- EVENTOS DE FOCO ----------
# Se disparan cuando el widget gana o pierde el foco

"<FocusIn>"         # El widget recibe el foco
"<FocusOut>"        # El widget pierde el foco


# --------- EVENTOS DE LA VENTANA ----------
# Relacionados con el estado o cambios de la ventana

"<Configure>"       # Cuando cambia tamaño o posición
"<Destroy>"         # Cuando el widget se destruye
"<Map>"             # Cuando el widget se hace visible
"<Unmap>"           # Cuando el widget se oculta
"<Visibility>"      # Cambio de visibilidad
"<Expose>"          # Redibujo del widget (visible)


# --------- EVENTOS DE ARRASTRE / COMBINACIONES ----------
# Se disparan con arrastre o combinaciones de mouse + teclas

"<B1-Motion>"        # Arrastrar con botón izquierdo presionado
"<B2-Motion>"        # Arrastrar con botón central
"<B3-Motion>"        # Arrastrar con botón derecho

"<Control-Button-1>" # Ctrl + clic izquierdo
"<Shift-Button-1>"   # Shift + clic izquierdo
"<Alt-Button-1>"     # Alt + clic izquierdo

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
