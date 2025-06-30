import json

# Lee y devuelve el contenido del archivo JSON como diccionario
def get():
    with open("E_Docente/database.json", "r") as file:
        data = json.load(file)
    return data

# Guarda los cambios en el archivo JSON
def rewrite(cambios):
    with open("E_Docente/database.json", "w") as file:
        json.dump(cambios, file, indent=4)


#------------------------------------------------------------- Admin view
# Verifica si los datos del login son correctos
# Usado en: View index (login)
def login(nombre, contra):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == nombre and usuario["password"] == contra and usuario["estado"] == 1:
            return True
    return False

#Obtener nonbre de la cuenta para el mensaje de bienvenido
# Usado en: View index (login)
def obtener_nombre(user):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == user:
            return usuario["nombre"]
    return False

# Verifica si el usuario es administrador
# Usado en: View index (login)
def es_admin(nombre):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == nombre and usuario["tipo"] == 1:
            return True
    return False


#-------------------------------------------------------------- View inicio de admin
# Obtiene el ciclo que esté activo
# Usado en: View inicio_admin, View inicio_estudiante, View resultados, View detalles_resultado, View evaluacion
def obtener_ciclo_activo():
    data = get()
    for ciclo in data["ciclos"]:
        if ciclo["estado"] == 1:
            return ciclo
    return None

# Cambia el estado de evaluación activa de un ciclo
# Usado en: View inicio_admin
def cambiar_estado_evaluacion(ciclo_id, activo):
    data = get()
    for ciclo in data["ciclos"]:
        if ciclo["id"] == ciclo_id:
            ciclo["evaluacion_activa"] = activo
            rewrite(data)
            return f"Evaluación del ciclo {ciclo[1]} ha sido {'activada' if activo == 1 else 'desactivada'}"
    return "Ciclo no encontrado"


#----------------------------------------------------------- View docente
# Devuelve True si un profesor ya existe, de lo contrario devuelve False.
# Usado en: View docentes
def profe_ya_existe(nombre):
    data = get()
    docentes = data["docentes"]

    for docente in docentes:
        if nombre == docente["nombre"]:
            return True
    return False

# Agrega un nuevo profesor a la base de datos
# Usado en: View docentes
def agregar_profesor(nombre):
    data = get()
    docentes = data["docentes"]

    id = len(docentes) + 1
    nuevo_docente = {
        "id": id,
        "nombre": nombre,
        "estado": 1,
        "materias": []
    }
    docentes.append(nuevo_docente)
    rewrite(data)


#----------------------------------------------------------- View estudiante
# Crea un nuevo usuario si la cuenta no existe ya
# Usado en: View estudiantes
def crear_usuario(cuenta, password, tipo, nombre):
    data = get()
    usuarios = data["usuarios"]

    if cuenta_ya_existe(cuenta):
        print("La cuenta ya existe mi broda")
        return

    id = len(usuarios)
    carnet = f"{id:06d}"  # Genera un carnet con 6 dígitos
    nuevo_usuario = {
        "id": id,
        "cuenta": cuenta,
        "password": password,
        "tipo": tipo,
        "estado": 1,
        "nombre": nombre,
        "carnet": carnet,
        "materias": []
    }
    usuarios.append(nuevo_usuario)
    rewrite(data)

# Verifica si una cuenta ya existe
# Usado en: View estudiantes
def cuenta_ya_existe(cuenta):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if cuenta == usuario["cuenta"]:
            return True
    return False


#----------------------------------------------------------- View materias
# Agrega una nueva materia a la base de datos
# Usado en: View materias
def agregar_materia(codigo, nombre):
    data = get()
    materias = data["materias"]

    id = len(materias) + 101  # IDs inician en 101
    nueva_materia = {
        "id": id,
        "codigo": codigo,
        "nombre": nombre,
        "estado": 1,
        "docentes": [],
        "estudiantes": []
    }
    materias.append(nueva_materia)
    rewrite(data)

# Verifica si una materia ya existe por su código
# Usado en: View materias
def materia_ya_existe(codigo):
    data = get()
    materias = data["materias"]

    for materia in materias:
        if codigo == materia["codigo"]:
            return True
    return False


#----------------------------------------------------------- View docente / View materias
# Asigna una materia a un profesor y viceversa
# Usado en: View docentes, View editar_docente, View editar_materia
def asignar_materia_a_profesor(profesor_id, materia_id):
    data = get()
    docentes = data["docentes"]
    materias = data["materias"]

    # Añade la materia al docente si no la tiene
    for docente in docentes:
        if docente["id"] == profesor_id and materia_id not in docente["materias"]:
            docente["materias"].append(materia_id)
            break

    # Añade el docente a la materia si no está registrado
    for materia in materias:
        if materia["id"] == materia_id and profesor_id not in materia["docentes"]:
            materia["docentes"].append(profesor_id)
            break

    rewrite(data)


#----------------------------------------------------------- View evaluacion
# Guarda una nueva evaluación en la base de datos
# Usado en: View evaluacion
def hacer_encuesta(clase, profesor, ciclo, respuestas, comentario, like, dislike):
    data = get()
    evaluaciones = data["evaluaciones"]

    id = len(evaluaciones) + 5001
    nueva_encuesta = {
        "id": id,
        "clase": clase,
        "profesor": profesor,
        "ciclo": ciclo,
        "respuestas": respuestas,
        "comentario": comentario,
        "like": like,
        "dislike": dislike
    }
    evaluaciones.append(nueva_encuesta)
    rewrite(data)

# Registra que un estudiante ya realizó una evaluación
# Usado en: View evaluacion
def registrar_evaluacion_realizada(estudiante_id, profesor_id, materia_id, ciclo):
    data = get()
    evaluaciones_realizadas = data["evaluaciones_realizadas"]

    nueva = {
        "estudiante_id": estudiante_id,
        "profesor_id": profesor_id,
        "materia_id": materia_id,
        "ciclo": ciclo
    }
    evaluaciones_realizadas.append(nueva)
    rewrite(data)


#----------------------------------------------------------- View inicio_estudiante
# Devuelve los profesores que el estudiante ya evaluó en cierto ciclo
# Usado en: View inicio_estudiante
def obtener_docentes_evaluados(estudiante_id, ciclo):
    data = get()
    evaluaciones = data["evaluaciones_realizadas"]

    evaluados = []
    for eval in evaluaciones:
        if eval["estudiante_id"] == estudiante_id and eval["ciclo"] == ciclo:
            evaluados.append((eval["profesor_id"], eval["materia_id"]))  # ✅ MATERIA también
    return evaluados


#----------------------------------------------------------- View resultados
# Devuelve todos los ciclos
# Usado en: View resultados, View detalles_resultado
def obtener_ciclos():
    data = get()
    return data.get("ciclos", [])


#----------------------------------------------------------- View resultados
# Genera resumen por docente (puntaje promedio, likes, dislikes, comentarios)
# Usado en: View resultados
def obtener_resumen_docentes(ciclo_id):
    data = get()
    docentes = data.get("docentes", [])
    materias = data.get("materias", [])
    evaluaciones = data.get("evaluaciones", [])

    resultado = []
    for docente in docentes:
        docente_id = docente["id"]
        materias_info = []
        suma_total = likes_total = dislikes_total = comentarios_total = total_respuestas = 0

        for materia in materias:
            if docente_id in materia.get("docentes", []):
                evals = [e for e in evaluaciones if e["profesor"] == docente_id and e["clase"] == materia["id"] and e["ciclo"] == ciclo_id]

                if not evals:
                    materias_info.append({
                        "id": materia["id"],
                        "codigo": materia["codigo"],
                        "nombre": materia["nombre"],
                        "promedio_puntaje": 0,
                        "likes": 0,
                        "dislikes": 0,
                        "comentarios": []
                    })
                    continue

                suma_materia = likes = dislikes = 0
                comentarios = []
                respuestas_totales = 0

                for e in evals:
                    respuestas = e.get("respuestas", {})
                    suma_materia += sum(respuestas.values())
                    respuestas_totales += len(respuestas)
                    likes += e.get("like", 0)
                    dislikes += e.get("dislike", 0)
                    comentario = e.get("comentario", "").strip()
                    if comentario:
                        comentarios.append(comentario)

                promedio = suma_materia / respuestas_totales if respuestas_totales > 0 else 0

                materias_info.append({
                    "id": materia["id"],
                    "codigo": materia["codigo"],
                    "nombre": materia["nombre"],
                    "promedio_puntaje": round(promedio, 2),
                    "likes": likes,
                    "dislikes": dislikes,
                    "comentarios": comentarios
                })

                suma_total += suma_materia
                likes_total += likes
                dislikes_total += dislikes
                comentarios_total += len(comentarios)
                total_respuestas += respuestas_totales

        promedio_general = suma_total / total_respuestas if total_respuestas > 0 else 0

        resultado.append({
            "id": docente_id,
            "nombre": docente["nombre"],
            "materias": materias_info,
            "promedio_general": round(promedio_general, 2),
            "likes_totales": likes_total,
            "dislikes_totales": dislikes_total,
            "comentarios_totales": comentarios_total
        })

    return resultado


#----------------------------------------------------------- View detalles_resultado
# Obtiene promedios por pregunta y comentarios para un docente en una materia y ciclo específico
# Usado en: View detalles_resultado
def obtener_promedios_y_comentarios(id_docente, id_materia, id_ciclo):
    data = get()
    evaluaciones = data.get("evaluaciones", [])

    evals = [e for e in evaluaciones if e["profesor"] == id_docente and e["clase"] == id_materia and e["ciclo"] == id_ciclo]

    if not evals:
        return {"promedios": {}, "comentarios": []}

    preguntas = set()
    for e in evals:
        preguntas.update(e["respuestas"].keys())

    suma = {p: 0 for p in preguntas}
    conteo = {p: 0 for p in preguntas}
    comentarios = []

    for e in evals:
        for p in preguntas:
            if p in e["respuestas"]:
                suma[p] += e["respuestas"][p]
                conteo[p] += 1
        comentario = e.get("comentario", "").strip()
        if comentario:
            comentarios.append(comentario)

    promedios = {}
    for p in preguntas:
        if conteo[p] > 0:
            promedios[p] = round(suma[p] / conteo[p], 2)
        else:
            promedios[p] = None

    return {
        "promedios": promedios,
        "comentarios": comentarios
    }


#----------------------------------------------------------- View estudiantes
# Devuelve cuántas evaluaciones ha hecho un estudiante y cuántas debe hacer
# Usado en: View estudiantes
def obtener_estado_evaluacion_estudiante(estudiante_id):
    data = get()
    usuarios = data.get("usuarios", [])
    materias = data.get("materias", [])
    docentes = data.get("docentes", [])
    evaluaciones_realizadas = data.get("evaluaciones_realizadas", [])

    # Buscar el estudiante por su ID
    estudiante = None
    for u in usuarios:
        if u.get("id") == estudiante_id:
            estudiante = u
            break

    if not estudiante:
        return (0, 0)

    total = 0
    for mat_id in estudiante.get("materias", []):
        mat = None
        for m in materias:
            if m.get("id") == mat_id:
                mat = m
                break
        if mat:
            total += len(mat.get("docentes", []))

    realizadas = 0
    for ev in evaluaciones_realizadas:
        if ev.get("estudiante_id") == estudiante_id:
            realizadas += 1

    return (realizadas, total)

