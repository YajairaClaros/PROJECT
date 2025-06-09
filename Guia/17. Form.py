#17 - Creación de un formulario
import tkinter as tk
from tkinter import ttk, messagebox
import json


ventana = tk.Tk()
ventana.title("Formulario completo sobre el espacio")
ventana.geometry("600x800")


# -------------------- Variables de control --------------------
nombre_var = tk.StringVar()
edad_var = tk.IntVar()
planeta_fav_var = tk.StringVar()
viajar_espacio_var = tk.BooleanVar()
nivel_interes_var = tk.StringVar()
escala_conocimiento_var = tk.DoubleVar()
lista_seleccionada = tk.StringVar()

# -------------------- Función para guardar en JSON --------------------

def guardar():
    seleccion = listbox.curselection()
    seleccion_lista = listbox.get(seleccion[0]) if seleccion else ""

    datos = {
        "nombre": nombre_var.get(),
        "edad": edad_var.get(),
        "planeta_favorito": planeta_fav_var.get(),
        "viajar_al_espacio": viajar_espacio_var.get(),
        "nivel_interes": nivel_interes_var.get(),
        "tema_favorito": seleccion_lista,
        "conocimiento_espacial": escala_conocimiento_var.get(),
        "comentarios": comentarios_text.get("1.0", tk.END).strip()
    }

    with open("formulario_completo_espacio.json", "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

    messagebox.showinfo("Guardado", "Respuestas guardadas correctamente.")

# -------------------- Título --------------------

tk.Label(ventana, text="Formulario: Exploración del espacio", font=("Arial", 16, "bold")).pack(pady=10)

# -------------------- Nombre (Entry) --------------------

tk.Label(ventana, text="1. ¿Cuál es tu nombre?").pack(anchor="w", padx=20)
tk.Entry(ventana, textvariable=nombre_var).pack(fill="x", padx=20, pady=5)

# -------------------- Edad (Spinbox) --------------------

tk.Label(ventana, text="2. ¿Cuál es tu edad?").pack(anchor="w", padx=20)
tk.Spinbox(ventana, from_=5, to=120, textvariable=edad_var).pack(fill="x", padx=20, pady=5)

# -------------------- Planeta favorito (Combobox) --------------------

tk.Label(ventana, text="3. ¿Cuál es tu planeta favorito?").pack(anchor="w", padx=20)
ttk.Combobox(ventana, values=[
    "Mercurio", "Venus", "Tierra", "Marte", "Júpiter", "Saturno", "Urano", "Neptuno"
], textvariable=planeta_fav_var, state="readonly").pack(fill="x", padx=20, pady=5)

# -------------------- ¿Viajarías al espacio? (Checkbutton) --------------------

tk.Checkbutton(ventana, text="4. ¿Te gustaría viajar al espacio?", variable=viajar_espacio_var).pack(anchor="w", padx=20, pady=10)

# -------------------- Nivel de interés (Radiobutton) --------------------

tk.Label(ventana, text="5. ¿Qué tanto te interesa el espacio?").pack(anchor="w", padx=20)
for nivel in ["Poco", "Moderado", "Mucho", "Pasión total"]:
    tk.Radiobutton(ventana, text=nivel, value=nivel, variable=nivel_interes_var).pack(anchor="w", padx=40)

# -------------------- Tema favorito del espacio (Listbox) --------------------

tk.Label(ventana, text="6. ¿Cuál es tu tema favorito del espacio?").pack(anchor="w", padx=20)
listbox = tk.Listbox(ventana, height=4)
temas = ["Agujeros negros", "Estrellas", "Exoplanetas", "Misiones espaciales", "Nebulosas"]
for tema in temas:
    listbox.insert(tk.END, tema)
listbox.pack(fill="x", padx=20, pady=5)

# -------------------- Conocimiento espacial (Scale) --------------------

tk.Label(ventana, text="7. ¿Qué tanto sabes sobre el espacio? (0 = nada, 10 = experto)").pack(anchor="w", padx=20)
tk.Scale(ventana, from_=0, to=10, orient="horizontal", variable=escala_conocimiento_var).pack(fill="x", padx=20, pady=5)

# -------------------- Comentarios (Text) --------------------

tk.Label(ventana, text="8. Comentarios adicionales:").pack(anchor="w", padx=20)
comentarios_text = tk.Text(ventana, height=4)
comentarios_text.pack(fill="both", padx=20, pady=5)

# -------------------- Botón Guardar (Button) --------------------

tk.Button(ventana, text="Guardar respuestas", bg="green", fg="white", command=guardar).pack(pady=20)

ventana.mainloop()
