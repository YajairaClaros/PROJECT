
import json

# Devuelve un diccionario copiado del json de datos.
def get():
    with open("E_Docente/database.json", "r") as file:
        data = json.load(file)
    return data

# Reescribe los cambios realizados al archivo de base de datos.
def rewrite(cambios):
    with open("E_Docente/database.json", "w") as file:
        json.dump(cambios, file, indent=4)
    return None

# Agrega una materia a la base de datos.
def agregar_materia(codigo, nombre):
    data = get()
    materias = data["materias"]

    id = len(materias) + 101
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


# Devuelve True si una materia ya existe, de lo contrario devuelve False.
def materia_ya_existe(codigo):
    data = get()
    materias = data["materias"]

    for materia in materias:
        if codigo == materia["codigo"]:
            return True
    return False



# Agrega un profesor a la base de datos.
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
    return None

# Asigna una materia a un profesor.
def asignar_materia_a_profesor(profesor_id, materia_id):
    data = get()
    docentes = data["docentes"]
    materias = data["materias"]

    for docente in docentes:
        if docente["id"] == profesor_id:
            if materia_id not in docente["materias"]:
                docente["materias"].append(materia_id)
                break

    for materia in materias:
        if materia["id"] == materia_id:
            if profesor_id not in materia["docentes"]:
                materia["docentes"].append(profesor_id)
                break

    rewrite(data)
    return None

# Asigna una materia a un estudiante.
def asignar_materia_a_estudiante(estudiante_id, materia_id):
    data = get()
    usuarios = data["usuarios"]
    materias = data["materias"]

    for usuario in usuarios:
        if usuario["id"] == estudiante_id:
            if materia_id not in usuario["materias"]:
                usuario["materias"].append(materia_id)
                break

    for materia in materias:
        if materia["id"] == materia_id:
            if estudiante_id not in materia["estudiantes"]:
                materia["estudiantes"].append(estudiante_id)
                break

    rewrite(data)
    return None

# Guarda el resultado de una encuesta en la base de datos.
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
    return None

# Registra que un estudiante ha realizado una evaluación.
def registrar_evaluacion_realizada(estudiante_id, profesor_id, materia_id, ciclo):
    data = get()
    evaluaciones_realizadas = data["evaluaciones_realizadas"]

    nueva_evaluacion_realizada = {
        "estudiante_id": estudiante_id,
        "profesor_id": profesor_id,
        "materia_id": materia_id,
        "ciclo": ciclo
    }
    evaluaciones_realizadas.append(nueva_evaluacion_realizada)
    rewrite(data)
    return None

# Devuelve True si se logra un loggeo correcto (nombre correcto y contraseña correcta), de lo contrario devuelve False.
def login(nombre, contra):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == nombre and usuario["password"] == contra:
            return True
    return False


# Devuelve True si un usuario pertenece al tipo "administrador".
def es_admin(nombre):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == nombre and usuario["tipo"] == 1:
            return True
    return False

# Obtiene los docentes evaluados por un estudiante en un ciclo específico.
def obtener_docentes_evaluados(estudiante_id, ciclo):
    data = get()
    evaluaciones_realizadas = data["evaluaciones_realizadas"]

    evaluados = [eval["profesor_id"] for eval in evaluaciones_realizadas if eval["estudiante_id"] == estudiante_id and eval["ciclo"] == ciclo]
    return evaluados

# Obtiene los docentes que un estudiante aún no ha evaluado en un ciclo específico.
def obtener_docentes_faltantes(estudiante_id, ciclo):
    data = get()
    usuarios = data["usuarios"]
    materias = data["materias"]

    estudiante = next((usuario for usuario in usuarios if usuario["id"] == estudiante_id), None)
    if not estudiante:
        return []

    evaluados = obtener_docentes_evaluados(estudiante_id, ciclo)
    faltantes = []

    for materia_id in estudiante["materias"]:
        materia = next((mat for mat in materias if mat["id"] == materia_id), None)
        if materia:
            for docente_id in materia["docentes"]:
                if docente_id not in evaluados:
                    faltantes.append(docente_id)

    return faltantes

# Obtiene estadísticas de un docente en un ciclo específico.
def obtener_estadisticas_docente(profesor_id, ciclo):
    data = get()
    evaluaciones = data["evaluaciones"]

    evaluaciones_docente = [eval for eval in evaluaciones if eval["profesor"] == profesor_id and eval["ciclo"] == ciclo]

    total_likes = sum(eval["like"] for eval in evaluaciones_docente)
    total_dislikes = sum(eval["dislike"] for eval in evaluaciones_docente)
    total_comentarios = len([eval for eval in evaluaciones_docente if eval["comentario"]])
    total_puntaje = sum(sum(eval["respuestas"].values()) for eval in evaluaciones_docente)
    promedio_puntaje = total_puntaje / len(evaluaciones_docente) if evaluaciones_docente else 0

    return {
        "total_likes": total_likes,
        "total_dislikes": total_dislikes,
        "total_comentarios": total_comentarios,
        "total_puntaje": total_puntaje,
        "promedio_puntaje": promedio_puntaje
    }

# Obtiene los estudiantes que no han completado sus evaluaciones a todos los docentes en un ciclo específico.
def obtener_estudiantes_con_evaluaciones_incompletas(ciclo):
    data = get()
    usuarios = data["usuarios"]
    evaluaciones_realizadas = data["evaluaciones_realizadas"]

    estudiantes_incompletos = []

    for usuario in usuarios:
        if usuario["tipo"] == 0:  # Es estudiante
            evaluados = obtener_docentes_evaluados(usuario["id"], ciclo)
            faltantes = obtener_docentes_faltantes(usuario["id"], ciclo)
            if faltantes:
                estudiantes_incompletos.append({
                    "estudiante_id": usuario["id"],
                    "nombre": usuario["nombre"],
                    "evaluados": len(evaluados),
                    "faltantes": len(faltantes)
                })

    return estudiantes_incompletos

def obtener_ciclo_activo():
    data = get()
    ciclos = data["ciclos"]
    for ciclo in ciclos:
        if ciclo["estado"] == 1:
            return ciclo
    return None  # Si no hay ciclo activo

def cambiar_ciclo_activo(nuevo_ciclo_id):
    data = get()
    ciclos = data["ciclos"]

    for ciclo in ciclos:
        ciclo["estado"] = 1 if ciclo["id"] == nuevo_ciclo_id else 0

    rewrite(data)
    return f"Ciclo activo cambiado al ID {nuevo_ciclo_id}"

def cambiar_estado_evaluacion(ciclo_id, activo):
    data = get()
    for ciclo in data["ciclos"]:
        if ciclo["id"] == ciclo_id:
            ciclo["evaluacion_activa"] = activo
            rewrite(data)
            return f"Evaluación del ciclo {ciclo[1]} ha sido {'activada' if activo == 1 else 'desactivada'}"
    return "Ciclo no encontrado"



#Funciones que no se usaron

''' 
# Crea un usuario en la base datos, asignando un nombre, una contraseña y un tipo (estudiante o administrador).
def crear_usuario(cuenta, password, tipo, nombre):
    data = get()
    usuarios = data["usuarios"]

    if cuenta_ya_existe(cuenta):
        print("La cuenta ya existe mi broda")
        return None
    else:
        id = len(usuarios)
        carnet = f"{id:06d}"
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
    return None

#Devuelve True si una cuenta ya existe, de lo contrario devuelve False.
def cuenta_ya_existe(cuenta):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if cuenta == usuario["cuenta"]:
            return True
    return False

# Elimina un profesor de la lista de profesores asignados a una materia en la base de datos.
def eliminar_profesor(profesor_id):
    data = get()
    materias = data["materias"]

    for materia in materias:
        if profesor_id in materia["docentes"]:
            materia["docentes"].remove(profesor_id)

    rewrite(data)
    return None

# Elimina una materia del diccionario de materias en la base de datos.
def eliminar_materia(materia_id):
    data = get()
    materias = data["materias"]

    materias = [materia for materia in materias if materia["id"] != materia_id]
    data["materias"] = materias

    rewrite(data)
    return None

# Devuelve True si un profesor ya existe, de lo contrario devuelve False.
def profe_ya_existe(nombre):
    data = get()
    docentes = data["docentes"]

    for docente in docentes:
        if nombre == docente["nombre"]:
            return True
    return False

'''