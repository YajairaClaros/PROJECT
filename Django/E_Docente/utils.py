
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
        if usuario["cuenta"] == nombre and usuario["password"] == contra and usuario["estado"] == 1:
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
def obtener_estadisticas_docente(profesor_id, ciclo, materia_id=None):
    data = get()
    evaluaciones = data["evaluaciones"]

    # Filtrar por profesor y ciclo
    evaluaciones_docente = [eval for eval in evaluaciones if eval["profesor"] == profesor_id and eval["ciclo"] == ciclo]

    # Si materia_id se pasa, filtrar también por materia (clase)
    if materia_id is not None:
        evaluaciones_docente = [eval for eval in evaluaciones_docente if eval["clase"] == materia_id]

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

def obtener_ciclos():
    data = get()
    return data.get("ciclos", [])



def cambiar_estado_evaluacion(ciclo_id, activo):
    data = get()
    for ciclo in data["ciclos"]:
        if ciclo["id"] == ciclo_id:
            ciclo["evaluacion_activa"] = activo
            rewrite(data)
            return f"Evaluación del ciclo {ciclo[1]} ha sido {'activada' if activo == 1 else 'desactivada'}"
    return "Ciclo no encontrado"




#--------------------IDK
def obtener_resumen_docentes(ciclo_id):
    data = get()
    docentes = data.get("docentes", [])
    materias = data.get("materias", [])
    evaluaciones = data.get("evaluaciones", [])

    resultado = []

    for docente in docentes:
        docente_id = docente["id"]
        docente_nombre = docente["nombre"]
        materias_docente = [m for m in materias if docente_id in m.get("docentes", [])]

        materias_info = []
        acumulador_puntaje = 0
        acumulador_likes = 0
        acumulador_dislikes = 0
        acumulador_comentarios = 0
        total_evaluaciones = 0

        for materia in materias_docente:
            materia_id = materia["id"]

            # Filtrar evaluaciones para este docente, materia y ciclo
            evals_filtradas = [
                e for e in evaluaciones
                if e["profesor"] == docente_id and e["clase"] == materia_id and e["ciclo"] == ciclo_id
            ]

            if not evals_filtradas:
                # No evaluaciones para esta materia en este ciclo
                materias_info.append({
                    "id": materia_id,
                    "codigo": materia["codigo"],
                    "nombre": materia["nombre"],
                    "promedio_puntaje": 0,
                    "likes": 0,
                    "dislikes": 0,
                    "comentarios": []
                })
                continue

            # Puntaje total y conteo
            suma_puntaje_materia = 0
            cuenta_respuestas = 0
            likes_materia = 0
            dislikes_materia = 0
            comentarios_materia = []

            for e in evals_filtradas:
                respuestas = e.get("respuestas", {})
                suma_puntaje_materia += sum(respuestas.values())
                cuenta_respuestas += len(respuestas)
                likes_materia += e.get("like", 0)
                dislikes_materia += e.get("dislike", 0)
                comentario = e.get("comentario", "").strip()
                if comentario:
                    comentarios_materia.append(comentario)

            promedio_puntaje_materia = (suma_puntaje_materia / cuenta_respuestas) if cuenta_respuestas > 0 else 0

            materias_info.append({
                "id": materia_id,
                "codigo": materia["codigo"],
                "nombre": materia["nombre"],
                "promedio_puntaje": round(promedio_puntaje_materia, 2),
                "likes": likes_materia,
                "dislikes": dislikes_materia,
                "comentarios": comentarios_materia
            })

            acumulador_puntaje += suma_puntaje_materia
            acumulador_likes += likes_materia
            acumulador_dislikes += dislikes_materia
            acumulador_comentarios += len(comentarios_materia)
            total_evaluaciones += cuenta_respuestas

        promedio_general = (acumulador_puntaje / total_evaluaciones) if total_evaluaciones > 0 else 0

        resultado.append({
            "id": docente_id,
            "nombre": docente_nombre,
            "materias": materias_info,
            "promedio_general": round(promedio_general, 2),
            "likes_totales": acumulador_likes,
            "dislikes_totales": acumulador_dislikes,
            "comentarios_totales": acumulador_comentarios
        })

    return resultado


def obtener_detalle_resultados(docente_id, ciclo_id):
    data = get()
    docentes = data.get("docentes", [])
    materias = data.get("materias", [])

    docente = next((d for d in docentes if d["id"] == docente_id), None)
    if not docente:
        return None  # Docente no encontrado

    # Materias del docente
    materias_docente = [m for m in materias if m["id"] in docente.get("materias", [])]

    # Para cada materia obtener puntajes por pregunta y comentarios (usando funciones que ya tienes)
    detalle_materias = []
    for materia in materias_docente:
        preguntas = obtener_puntajes_por_pregunta(docente_id, materia["id"], ciclo_id)
        comentarios = obtener_comentarios(docente_id, materia["id"], ciclo_id)
        detalle_materias.append({
            "id": materia["id"],
            "nombre": materia["nombre"],
            "puntajes_por_pregunta": preguntas,
            "comentarios": comentarios
        })

    return {
        "docente_id": docente["id"],
        "nombre": docente["nombre"],
        "ciclo_id": ciclo_id,
        "materias": detalle_materias
    }



def obtener_puntaje_promedio(docente_id, materia_id, ciclo_id):
    """
    Devuelve el promedio total de puntajes para todas las preguntas
    de todas las encuestas hechas para un docente, materia y ciclo específicos.
    """
    data = get()  # Tu función para obtener todo el JSON
    encuestas = data.get("encuestas", [])

    # Filtrar encuestas que coincidan con docente, materia y ciclo
    puntajes_totales = 0
    conteo_puntajes = 0

    for encuesta in encuestas:
        if (
            encuesta["profesor"] == docente_id
            and encuesta["clase"] == materia_id
            and encuesta["ciclo"] == ciclo_id
        ):
            respuestas = encuesta.get("respuestas", {})
            for val in respuestas.values():
                puntajes_totales += val
                conteo_puntajes += 1

    if conteo_puntajes == 0:
        return 0

    promedio = puntajes_totales / conteo_puntajes
    return round(promedio, 2)


def obtener_likes(docente_id, materia_id, ciclo_id):
    data = get()
    encuestas = data.get("encuestas", [])
    total_likes = sum(
        encuesta.get("like", 0)
        for encuesta in encuestas
        if encuesta["profesor"] == docente_id
        and encuesta["clase"] == materia_id
        and encuesta["ciclo"] == ciclo_id
    )
    return total_likes


def obtener_dislikes(docente_id, materia_id, ciclo_id):
    data = get()
    encuestas = data.get("encuestas", [])
    total_dislikes = sum(
        encuesta.get("dislike", 0)
        for encuesta in encuestas
        if encuesta["profesor"] == docente_id
        and encuesta["clase"] == materia_id
        and encuesta["ciclo"] == ciclo_id
    )
    return total_dislikes


def obtener_comentarios(docente_id, materia_id, ciclo_id):
    data = get()
    encuestas = data.get("encuestas", [])
    comentarios = [
        encuesta.get("comentario", "")
        for encuesta in encuestas
        if encuesta["profesor"] == docente_id
        and encuesta["clase"] == materia_id
        and encuesta["ciclo"] == ciclo_id
        and encuesta.get("comentario", "").strip() != ""
    ]
    return comentarios


def obtener_puntajes_por_pregunta(docente_id, materia_id, ciclo_id):
    """
    Retorna lista de (numero_pregunta, promedio) para las 20 preguntas (o las que haya).
    """
    data = get()
    encuestas = data.get("encuestas", [])

    # Sumar puntajes por pregunta
    suma_preguntas = {}
    conteo_preguntas = {}

    for encuesta in encuestas:
        if (
            encuesta["profesor"] == docente_id
            and encuesta["clase"] == materia_id
            and encuesta["ciclo"] == ciclo_id
        ):
            respuestas = encuesta.get("respuestas", {})
            for pregunta, puntaje in respuestas.items():
                try:
                    num_pregunta = int(pregunta.replace("pregunta", ""))
                except Exception:
                    continue
                suma_preguntas[num_pregunta] = suma_preguntas.get(num_pregunta, 0) + puntaje
                conteo_preguntas[num_pregunta] = conteo_preguntas.get(num_pregunta, 0) + 1

    resultado = []
    for num in sorted(suma_preguntas.keys()):
        promedio = suma_preguntas[num] / conteo_preguntas[num]
        resultado.append((num, round(promedio, 2)))

    return resultado


def obtener_ciclos():
    data = get()
    return data.get("ciclos", [])


def obtener_ciclo_por_id(ciclo_id):
    data = get()
    ciclos = data.get("ciclos", [])
    for ciclo in ciclos:
        if ciclo["id"] == ciclo_id:
            return ciclo
    return None


def obtener_promedios_y_comentarios(id_docente, id_materia, id_ciclo):
    data = get()
    evaluaciones = data.get("evaluaciones", [])

    # Filtrar evaluaciones que coincidan en docente, materia y ciclo
    evaluaciones_filtradas = [
        e for e in evaluaciones
        if e["profesor"] == id_docente and e["clase"] == id_materia and e["ciclo"] == id_ciclo
    ]

    if not evaluaciones_filtradas:
        return {
            "promedios": {},
            "comentarios": []
        }

    # Inicializar acumuladores para cada pregunta
    preguntas = set()
    for e in evaluaciones_filtradas:
        preguntas.update(e["respuestas"].keys())

    suma_preguntas = {p: 0 for p in preguntas}
    conteo_preguntas = {p: 0 for p in preguntas}
    comentarios = []

    for e in evaluaciones_filtradas:
        respuestas = e.get("respuestas", {})
        for p in preguntas:
            if p in respuestas:
                suma_preguntas[p] += respuestas[p]
                conteo_preguntas[p] += 1
        comentario = e.get("comentario", "").strip()
        if comentario:
            comentarios.append(comentario)

    # Calcular promedio por pregunta
    promedios = {}
    for p in preguntas:
        if conteo_preguntas[p] > 0:
            promedios[p] = round(suma_preguntas[p] / conteo_preguntas[p], 2)
        else:
            promedios[p] = None  # o 0, según prefieras

    return {
        "promedios": promedios,
        "comentarios": comentarios
    }


#Funciones que no se usaron

''' 
def cambiar_ciclo_activo(nuevo_ciclo_id):
    data = get()
    ciclos = data["ciclos"]

    for ciclo in ciclos:
        ciclo["estado"] = 1 if ciclo["id"] == nuevo_ciclo_id else 0

    rewrite(data)
    return f"Ciclo activo cambiado al ID {nuevo_ciclo_id}"
    
# Crea un usuario en la base datos, asignando un nombre, una contraseña y un tipo (estudiante o administrador).


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