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

# Crea un nuevo usuario si la cuenta no existe ya
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
def cuenta_ya_existe(cuenta):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if cuenta == usuario["cuenta"]:
            return True
    return False

# Agrega una nueva materia a la base de datos
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
def materia_ya_existe(codigo):
    data = get()
    materias = data["materias"]

    for materia in materias:
        if codigo == materia["codigo"]:
            return True
    return False

# Agrega un nuevo profesor a la base de datos
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

# Asigna una materia a un profesor y viceversa
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

# Guarda una nueva evaluación en la base de datos
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

# Verifica si los datos del login son correctos
def login(nombre, contra):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == nombre and usuario["password"] == contra and usuario["estado"] == 1:
            return True
    return False

#Obtener nonbre de la cuenta para el mensaje de bienvenido
def obtener_nombre(user):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == user:
            return usuario["nombre"]
    return False



# Verifica si el usuario es administrador
def es_admin(nombre):
    data = get()
    usuarios = data["usuarios"]

    for usuario in usuarios:
        if usuario["cuenta"] == nombre and usuario["tipo"] == 1:
            return True
    return False

# Devuelve los profesores que el estudiante ya evaluó en cierto ciclo
# Devuelve una lista de tuplas (profesor_id, materia_id) evaluados por el estudiante en el ciclo
def obtener_docentes_evaluados(estudiante_id, ciclo):
    data = get()
    evaluaciones = data["evaluaciones_realizadas"]

    evaluados = []
    for eval in evaluaciones:
        if eval["estudiante_id"] == estudiante_id and eval["ciclo"] == ciclo:
            evaluados.append((eval["profesor_id"], eval["materia_id"]))  # ✅ MATERIA también
    return evaluados



# Obtiene el ciclo que esté activo
def obtener_ciclo_activo():
    data = get()
    for ciclo in data["ciclos"]:
        if ciclo["estado"] == 1:
            return ciclo
    return None

# Devuelve todos los ciclos
def obtener_ciclos():
    data = get()
    return data.get("ciclos", [])

# Cambia el estado de evaluación activa de un ciclo
def cambiar_estado_evaluacion(ciclo_id, activo):
    data = get()
    for ciclo in data["ciclos"]:
        if ciclo["id"] == ciclo_id:
            ciclo["evaluacion_activa"] = activo
            rewrite(data)
            return f"Evaluación del ciclo {ciclo[1]} ha sido {'activada' if activo == 1 else 'desactivada'}"
    return "Ciclo no encontrado"

# ---------------------- Reportes

# Genera resumen por docente (puntaje promedio, likes, dislikes, comentarios)
def obtener_resumen_docentes(ciclo_id):
    # Cargar los datos desde la base (docentes, materias y evaluaciones)
    data = get()
    docentes = data.get("docentes", [])
    materias = data.get("materias", [])
    evaluaciones = data.get("evaluaciones", [])

    resultado = []  # Lista donde se almacenará el resumen por docente

    for docente in docentes:
        docente_id = docente["id"]
        materias_info = []  # Lista de materias evaluadas por el docente
        # Inicializar contadores generales por docente
        suma_total = likes_total = dislikes_total = comentarios_total = total_respuestas = 0

        for materia in materias:
            # Verificar si el docente imparte esta materia
            if docente_id in materia.get("docentes", []):
                # Filtrar evaluaciones que correspondan a este docente, esta materia y ciclo
                evals = []
                for e in evaluaciones:
                    if e["profesor"] == docente_id and e["clase"] == materia["id"] and e["ciclo"] == ciclo_id:
                        evals.append(e)

                # Si no hay evaluaciones, agregar información vacía para esta materia
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
                    continue  # Pasar a la siguiente materia

                # Inicializar acumuladores por materia
                suma_materia = likes = dislikes = 0
                comentarios = []
                respuestas_totales = 0

                # Recorrer cada evaluación para acumular datos
                for e in evals:
                    respuestas = e.get("respuestas", {})
                    suma_materia += sum(respuestas.values())  # Sumar todos los puntajes
                    respuestas_totales += len(respuestas)  # Contar cuántas respuestas hubo
                    likes += e.get("like", 0)
                    dislikes += e.get("dislike", 0)

                    # Guardar el comentario si no está vacío
                    comentario = e.get("comentario", "").strip()
                    if comentario:
                        comentarios.append(comentario)

                # Calcular el promedio de la materia
                promedio = suma_materia / respuestas_totales if respuestas_totales > 0 else 0

                # Guardar la información acumulada de la materia
                materias_info.append({
                    "id": materia["id"],
                    "codigo": materia["codigo"],
                    "nombre": materia["nombre"],
                    "promedio_puntaje": round(promedio, 2),
                    "likes": likes,
                    "dislikes": dislikes,
                    "comentarios": comentarios
                })

                # Acumular totales generales del docente
                suma_total += suma_materia
                likes_total += likes
                dislikes_total += dislikes
                comentarios_total += len(comentarios)
                total_respuestas += respuestas_totales

        # Calcular promedio general del docente
        promedio_general = suma_total / total_respuestas if total_respuestas > 0 else 0

        # Guardar los resultados del docente
        resultado.append({
            "id": docente_id,
            "nombre": docente["nombre"],
            "materias": materias_info,
            "promedio_general": round(promedio_general, 2),
            "likes_totales": likes_total,
            "dislikes_totales": dislikes_total,
            "comentarios_totales": comentarios_total
        })

    return resultado  # Devuelve la lista con el resumen de todos los docentes


# Obtiene promedios por pregunta y comentarios para un docente en una materia y ciclo específico
def obtener_promedios_y_comentarios(id_docente, id_materia, id_ciclo):
    # Cargar datos desde la base
    data = get()
    evaluaciones = data.get("evaluaciones", [])

    # Filtrar evaluaciones que coincidan con el docente, la materia y el ciclo
    evals = []
    for e in evaluaciones:
        if e["profesor"] == id_docente and e["clase"] == id_materia and e["ciclo"] == id_ciclo:
            evals.append(e)

    # Si no hay evaluaciones, retornar valores vacíos
    if not evals:
        return {"promedios": {}, "comentarios": []}

    # Identificar todas las preguntas presentes en las evaluaciones
    preguntas = set()
    for e in evals:
        preguntas.update(e["respuestas"].keys())

    # Inicializar acumuladores por pregunta
    suma = {p: 0 for p in preguntas}
    conteo = {p: 0 for p in preguntas}
    comentarios = []

    # Recorrer evaluaciones para sumar puntajes y contar respuestas por pregunta
    for e in evals:
        for p in preguntas:
            if p in e["respuestas"]:
                suma[p] += e["respuestas"][p]
                conteo[p] += 1
        # Guardar comentario si no está vacío
        comentario = e.get("comentario", "").strip()
        if comentario:
            comentarios.append(comentario)

    # Calcular promedios por pregunta
    promedios = {}
    for p in preguntas:
        if conteo[p] > 0:
            promedios[p] = round(suma[p] / conteo[p], 2)
        else:
            promedios[p] = None  # Si no hay respuestas, dejar el promedio como None

    # Devolver promedios y comentarios
    return {
        "promedios": promedios,
        "comentarios": comentarios
    }


# Devuelve True si un profesor ya existe, de lo contrario devuelve False.
def profe_ya_existe(nombre):
    data = get()
    docentes = data["docentes"]

    for docente in docentes:
        if nombre == docente["nombre"]:
            return True
    return False

def obtener_estado_evaluacion_estudiante(estudiante_id):
    data = get()
    usuarios = data.get("usuarios", [])
    materias = data.get("materias", [])
    docentes = data.get("docentes", [])
    evaluaciones_realizadas = data.get("evaluaciones_realizadas", [])

    # Buscar el estudiante
    estudiante = next((u for u in usuarios if u["id"] == estudiante_id), None)
    if not estudiante:
        return (0, 0)  # No existe

    # Total evaluaciones posibles: sumamos todos los docentes de las materias del estudiante
    total = 0
    for mat_id in estudiante.get("materias", []):
        mat = next((m for m in materias if m["id"] == mat_id), None)
        if mat:
            total += len(mat.get("docentes", []))

    # Evaluaciones realizadas: contar registros en evaluaciones_realizadas donde
    # estudiante_id coincide con el dado
    realizadas = sum(1 for ev in evaluaciones_realizadas if ev.get("estudiante_id") == estudiante_id)

    return (realizadas, total)



#Funciones que no se usaron

''' 
# Devuelve los profesores que el estudiante aún no ha evaluado
def obtener_docentes_faltantes(estudiante_id, ciclo):
    data = get()
    usuarios = data["usuarios"]
    materias = data["materias"]

    estudiante = None
    for usuario in usuarios:
        if usuario["id"] == estudiante_id:
            estudiante = usuario
            break

    if not estudiante:
        return []

    evaluados = obtener_docentes_evaluados(estudiante_id, ciclo)
    faltantes = []

    for materia_id in estudiante["materias"]:
        for materia in materias:
            if materia["id"] == materia_id:
                for docente_id in materia["docentes"]:
                    if docente_id not in evaluados:
                        faltantes.append(docente_id)
                break

    return faltantes


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
    
def obtener_ciclo_por_id(ciclo_id):
    data = get()
    ciclos = data.get("ciclos", [])
    for ciclo in ciclos:
        if ciclo["id"] == ciclo_id:
            return ciclo
    return None
    
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

'''