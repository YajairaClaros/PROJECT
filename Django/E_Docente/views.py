from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import utils
from django.contrib.sessions.models import Session


# Vista para la página principal e inicio de sesión
def index(request):
    if request.method == "POST":  # -------------------------------> Proceso de inicio de sesión
        cuenta = request.POST.get("cuenta")
        password = request.POST.get("password")

        # Verificar credenciales con la función utils.login
        if utils.login(cuenta, password):
            # Guardar usuario en sesión para mantener sesión activa
            nombre_cuenta = utils.obtener_nombre(cuenta)
            request.session["usuario"] = cuenta
            request.session["nombre"] = nombre_cuenta

            # Verificar si el usuario es administrador
            if utils.es_admin(cuenta):
                return redirect("inicio_admin")  # Redirigir a panel admin
            else:
                return redirect("inicio_estudiante")  # Redirigir a panel estudiante
        else:
            # Credenciales incorrectas o usuario inactivo
            return render(request, "index.html", {"error": "Error: Usuario o contraseña incorrecta o usuario inactivo"})

    # Si no es POST, mostrar página de login
    return render(request, "index.html")


# Vista para el panel principal de administrador
def inicio_admin(request):
    # Si no hay usuario en sesión, redirigir a login
    if "usuario" not in request.session:
        return redirect("/")

    if request.method == "POST":
        try:
            # Obtener datos enviados para cambiar estado de evaluación
            id = int(request.POST.get("id"))
            estado = int(request.POST.get("estado"))

            # Cambiar estado de evaluación mediante utils
            utils.cambiar_estado_evaluacion(id, estado)

        except Exception as e:
            # Si ocurre error al modificar, mostrar mensaje de error en plantilla
            return render(request, 'admin/index.html', {
                'ciclo': utils.obtener_ciclo_activo(),
                'error': 'No se ha podido modificar el estado de la evaluación'
            })

    # Obtener ciclo activo para mostrar en la plantilla
    ciclo = utils.obtener_ciclo_activo()
    return render(request, 'admin/index.html', {'ciclo': ciclo})


# Vista para gestionar docentes
def docentes(request):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()
    docentes = data["docentes"]
    materias = data["materias"]

    error = None

    if request.method == "POST":
        nombre = request.POST.get("name")
        materia_id = request.POST.get("subject")

        # Verificar si docente ya existe para evitar duplicados
        if utils.profe_ya_existe(nombre):
            error = "El docente ya existe."
        else:
            # Crear nuevo docente
            utils.agregar_profesor(nombre)

            # Buscar el docente recién agregado para obtener su ID
            nuevo_docente = None
            for d in utils.get()["docentes"]:
                if d["nombre"] == nombre:
                    nuevo_docente = d
                    break

            # Si se tiene materia seleccionada, asignarla al docente
            if nuevo_docente and materia_id:
                utils.asignar_materia_a_profesor(nuevo_docente["id"], int(materia_id))

        return redirect("docentes")

    # Añadir lista con nombres de materias para cada docente (para mostrar en plantilla)
    for docente in docentes:
        docente["materias_nombres"] = []
        for mat in materias:
            if mat["id"] in docente["materias"]:
                docente["materias_nombres"].append(mat["nombre"])

    return render(request, "admin/docentes.html", {
        "docentes": docentes,
        "materias": materias,
        "error": error
    })


# Vista para editar un docente específico
def editar_docente(request, docente_id):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()
    docentes = data["docentes"]
    materias = data["materias"]

    # Buscar el docente por id
    docente = None
    for d in docentes:
        if d["id"] == docente_id:
            docente = d
            break

    if not docente:
        return redirect("docentes")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "actualizar":
            # Actualizar nombre y estado del docente
            docente["nombre"] = request.POST.get("name")
            docente["estado"] = int(request.POST.get("estado"))
            utils.rewrite(data)
            return redirect("docentes")

        elif action == "agregar_materia":
            # Agregar materia a docente si no está ya asignada
            materia_id = int(request.POST.get("subject"))
            utils.asignar_materia_a_profesor(docente_id, materia_id)
            return redirect("editar_docente", docente_id=docente_id)

        elif action == "quitar_materia":
            # Quitar materia asignada al docente
            materia_id = int(request.POST.get("materia_id"))
            if materia_id in docente["materias"]:
                docente["materias"].remove(materia_id)
            # También quitar docente de la materia
            for materia in materias:
                if materia["id"] == materia_id and docente_id in materia["docentes"]:
                    materia["docentes"].remove(docente_id)
            utils.rewrite(data)
            return redirect("editar_docente", docente_id=docente_id)

    # Listas de materias asignadas y disponibles para el docente (para mostrar en plantilla)
    materias_asignadas = []
    materias_disponibles = []

    for mat in materias:
        if mat["id"] in docente["materias"]:
            materias_asignadas.append(mat)
        else:
            materias_disponibles.append(mat)

    return render(request, "admin/editar_docente.html", {
        "docente": docente,
        "materias_asignadas": materias_asignadas,
        "materias": materias_disponibles,
    })


# Vista para gestionar estudiantes
def estudiantes(request):
    if "usuario" not in request.session:
        return redirect("/")

    error = None  # Variable para posibles errores

    if request.method == "POST":
        # Obtener datos enviados por formulario
        nombre = request.POST.get("name")
        cuenta = request.POST.get("cuenta")
        password = request.POST.get("password")

        # Verificar si cuenta ya existe para evitar duplicados
        if utils.cuenta_ya_existe(cuenta):
            error = "La cuenta ya existe, elige otro nombre de usuario."
        else:
            # Crear nuevo usuario tipo estudiante (tipo=0)
            utils.crear_usuario(cuenta, password, 0, nombre)
            return redirect("estudiantes")

    # Si no es POST o hubo error, obtener lista actualizada de estudiantes
    data = utils.get()
    estudiantes = []
    for u in data["usuarios"]:
        if u["tipo"] == 0:
            estudiantes.append(u)

    # Crear diccionario para obtener nombre de materia desde su id
    materias_dict = {}
    for m in data["materias"]:
        materias_dict[m["id"]] = m["nombre"]

    # Añadir lista de nombres de materias asignadas para cada estudiante
    for e in estudiantes:
        e["materias_nombres"] = []
        for mid in e["materias"]:
            nombre_materia = materias_dict.get(mid, "Desconocida")
            e["materias_nombres"].append(nombre_materia)
        # Agrega el progreso de evaluación como string "x/y"
        realizadas, total = utils.obtener_estado_evaluacion_estudiante(e["id"])
        e["evaluaciones_realizadas"] = f"{realizadas}/{total}" if total > 0 else "0/0"

    return render(request, 'admin/estudiantes.html', {
        "estudiantes": estudiantes,
        "error": error,
    })


# Vista para editar un estudiante específico
def editar_estudiante(request, id):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()  # Cargar base de datos
    estudiante = None
    for u in data["usuarios"]:
        if u["id"] == id:
            estudiante = u
            break

    materias = data["materias"]

    if not estudiante:
        return redirect("estudiantes")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "actualizar":
            # Actualizar datos básicos del estudiante
            estudiante["nombre"] = request.POST.get("name")
            estudiante["cuenta"] = request.POST.get("cuenta")
            estudiante["password"] = request.POST.get("password")
            estudiante["estado"] = int(request.POST.get("estado"))

        elif action == "agregar_materia":
            # Agregar materia al estudiante si no está asignada
            materia_id = request.POST.get("subject")
            if materia_id and materia_id.isdigit():
                materia_id = int(materia_id)
                if materia_id not in estudiante["materias"]:
                    estudiante["materias"].append(materia_id)

                    # Agregar estudiante a la materia correspondiente
                    for m in materias:
                        if m["id"] == materia_id and estudiante["id"] not in m["estudiantes"]:
                            m["estudiantes"].append(estudiante["id"])
                            break

        elif action == "quitar_materia":
            # Quitar materia asignada al estudiante
            materia_id = int(request.POST.get("materia_id"))
            if materia_id in estudiante["materias"]:
                estudiante["materias"].remove(materia_id)
                # También quitar estudiante de la materia
                for m in materias:
                    if m["id"] == materia_id and estudiante["id"] in m["estudiantes"]:
                        m["estudiantes"].remove(estudiante["id"])
                        break

        # Guardar cambios en la base de datos
        utils.rewrite(data)
        return redirect("editar_estudiante", id=id)

    # Materias asignadas actualmente al estudiante
    materias_asignadas = []
    for m in materias:
        if m["id"] in estudiante["materias"]:
            materias_asignadas.append(m)

    return render(request, "admin/editar_estudiante.html", {
        "estudiante": estudiante,
        "materias": materias,
        "materias_asignadas": materias_asignadas,
    })


# Vista para gestionar materias
def materias(request):
    if "usuario" not in request.session:
        return redirect("/")

    error = None

    if request.method == "POST":
        nombre = request.POST.get("name")
        codigo = request.POST.get("codigo")

        # Verificar si materia ya existe
        if utils.materia_ya_existe(codigo):
            error = "La materia ya existe."
        else:
            # Agregar materia nueva
            utils.agregar_materia(codigo, nombre)

        return redirect("materias")  # Prevenir reenvío del formulario

    data = utils.get()
    materias = data["materias"]
    docentes = data["docentes"]

    # Añadir lista de nombres de docentes para cada materia (para mostrar en plantilla)
    for mat in materias:
        mat["docentes_nombres"] = []
        for doc in docentes:
            if doc["id"] in mat["docentes"]:
                mat["docentes_nombres"].append(doc["nombre"])

    return render(request, "admin/materias.html", {
        "materias": materias,
        "docentes": docentes,
        "error": error
    })


# Vista para editar una materia específica
def editar_materia(request, id):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()
    materias = data["materias"]
    docentes = data["docentes"]

    # Buscar materia por id
    materia = None
    for m in materias:
        if m["id"] == id:
            materia = m
            break

    if not materia:
        return redirect("materias")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "actualizar":
            # Actualizar datos de la materia
            materia["nombre"] = request.POST.get("nombre")
            materia["codigo"] = request.POST.get("codigo")
            materia["estado"] = int(request.POST.get("estado"))
            utils.rewrite(data)
            return redirect("materias")

        elif action == "agregar_docente":
            # Asignar docente a materia
            docente_id = int(request.POST.get("docente_id"))
            utils.asignar_materia_a_profesor(docente_id, id)
            return redirect("editar_materia", id=id)

        elif action == "quitar_docente":
            # Quitar docente asignado a materia
            docente_id = int(request.POST.get("docente_id"))
            if docente_id in materia["docentes"]:
                materia["docentes"].remove(docente_id)
                # También quitar materia del docente
                for doc in docentes:
                    if doc["id"] == docente_id and id in doc["materias"]:
                        doc["materias"].remove(id)
                utils.rewrite(data)
            return redirect("editar_materia", id=id)

    # Listas de docentes asignados y disponibles para la materia
    docentes_asignados = []
    docentes_disponibles = []
    for doc in docentes:
        if doc["id"] in materia["docentes"]:
            docentes_asignados.append(doc)
        else:
            docentes_disponibles.append(doc)

    return render(request, "admin/editar_materia.html", {
        "materia": materia,
        "docentes_asignados": docentes_asignados,
        "docentes_disponibles": docentes_disponibles
    })


# Vista para mostrar resultados generales de evaluaciones
def resultados(request):
    if "usuario" not in request.session:
        return redirect("/")

    # Obtener ciclo seleccionado desde GET o usar ciclo activo por defecto
    ciclo_id = request.GET.get("ciclo_id")
    if ciclo_id and ciclo_id.isdigit():
        ciclo_id = int(ciclo_id)
    else:
        ciclo = utils.obtener_ciclo_activo()
        if ciclo:
            ciclo_id = ciclo["id"]
        else:
            ciclo_id = None

    resumen = []
    if ciclo_id:
        resumen_raw = utils.obtener_resumen_docentes(ciclo_id)

        # Preparar datos para la plantilla (simplificando la estructura)
        for d in resumen_raw:
            resumen.append({
                "id": d["id"],
                "nombre": d["nombre"],
                "materias": [
                    {"materia": m["nombre"], "puntaje": m["promedio_puntaje"]}
                    for m in d["materias"]
                ],
                "promedio": d["promedio_general"],
                "likes": d["likes_totales"],
                "dislikes": d["dislikes_totales"],
                "comentarios": d["comentarios_totales"],
            })

    ciclos = utils.obtener_ciclos()  # Para el selector de ciclos

    return render(request, 'admin/resultados.html', {
        "resumen": resumen,
        "ciclos": ciclos,
        "ciclo_seleccionado": ciclo_id,
    })


# Vista para mostrar detalles de resultados de un docente
def detalles_resultado(request, docente_id, ciclo_seleccionado_id):
    if "usuario" not in request.session:
        return redirect("/")


    ciclos = utils.obtener_ciclos()
    ciclo = None
    for c in ciclos:
        if c["id"] == ciclo_seleccionado_id:
            ciclo = c
    if not ciclo:
        return render(request, "admin/detalles_resultados.html", {"error": "No hay ciclo activo."})

    ciclo_id = ciclo["id"]

    data = utils.get()

    # Buscar docente por id
    docente = None
    for d in data["docentes"]:
        if d["id"] == docente_id:
            docente = d
            break

    if not docente:
        return redirect("resultados")

    # Listar materias del docente
    materias_docente = []
    for m in data["materias"]:
        if m["id"] in docente.get("materias", []):
            materias_docente.append(m)

    # Obtener materia seleccionada desde GET para mostrar detalle
    materia_seleccionada_id = request.GET.get("subject")
    if materia_seleccionada_id and materia_seleccionada_id.isdigit():
        materia_seleccionada_id = int(materia_seleccionada_id)
    else:
        materia_seleccionada_id = None

    detalle_materia = None
    if materia_seleccionada_id:
        resultado = utils.obtener_promedios_y_comentarios(docente_id, materia_seleccionada_id, ciclo_id)
        detalle_materia = {
            "id": materia_seleccionada_id,
            "nombre": "Materia"
        }
        # Buscar nombre real de la materia para mostrar
        for m in materias_docente:
            if m["id"] == materia_seleccionada_id:
                detalle_materia["nombre"] = m["nombre"]
                break

        detalle_materia["puntajes_por_pregunta"] = resultado["promedios"]
        detalle_materia["comentarios"] = resultado["comentarios"]

    return render(request, "admin/detalles_resultados.html", {
        "ciclo_nombre": ciclo["nombre"],
        "docente_id": docente["id"],
        "docente_nombre": docente["nombre"],
        "materias": materias_docente,
        "materia_seleccionada": detalle_materia
    })


# Vista para panel principal del estudiante
def inicio_estudiante(request):
    if "usuario" not in request.session:
        return redirect("/")

    cuenta = request.session["usuario"]

    data = utils.get()
    usuarios = data["usuarios"]
    materias = data["materias"]
    docentes = data["docentes"]

    # Buscar estudiante por cuenta y tipo
    estudiante = None
    for u in usuarios:
        if u["cuenta"] == cuenta and u["tipo"] == 0:
            estudiante = u
            break

    if not estudiante:
        return redirect("login")

    ciclo = utils.obtener_ciclo_activo()
    evaluados = utils.obtener_docentes_evaluados(estudiante["id"], ciclo["id"])

    evaluables = []
    # Preparar lista de docentes y materias que el estudiante puede evaluar
    for mat_id in estudiante["materias"]:
        materia = None
        for m in materias:
            if m["id"] == mat_id:
                materia = m
                break
        if not materia:
            continue

        for docente_id in materia["docentes"]:
            docente = None
            for d in docentes:
                if d["id"] == docente_id:
                    docente = d
                    break
            if not docente:
                continue

            ya_evaluado = (docente_id, materia["id"]) in evaluados
            evaluables.append({
                "docente": docente["nombre"],
                "materia": materia["nombre"],
                "evaluado": ya_evaluado,
                "materia_id": materia["id"],
                "docente_id": docente["id"]
            })

    return render(request, 'estudiante/index.html', {"evaluables": evaluables, "ciclo": ciclo})


# Vista para realizar una evaluación
def evaluacion(request, materia_id, docente_id):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()

    cuenta = request.session["usuario"]

    # Buscar estudiante por cuenta y tipo
    estudiante = None
    for u in data["usuarios"]:
        if u["cuenta"] == cuenta and u["tipo"] == 0:
            estudiante = u
            break

    if not estudiante:
        return redirect("inicio_estudiante")

    ciclo = utils.obtener_ciclo_activo()
    materia = None
    docente = None
    for m in data["materias"]:
        if m["id"] == materia_id:
            materia = m
            break
    for d in data["docentes"]:
        if d["id"] == docente_id:
            docente = d
            break

    if request.method == "POST":
        # Recoger respuestas de las preguntas enviadas (del 1 al 20)
        respuestas = {}
        for i in range(1, 21):
            key = f"pregunta{i}"
            if key in request.POST:
                try:
                    respuestas[key] = int(request.POST.get(key, 0))
                except Exception:
                    respuestas[key] = 0  # Valor por defecto

        comentario = request.POST.get("comentario", "")
        reaccion = request.POST.get("like_dislike", "0")

        # Transformar la reacción en valores numéricos de like/dislike
        try:
            reaccion = int(reaccion)
        except Exception:
            reaccion = 0

        like = 1 if reaccion == 1 else 0
        dislike = 1 if reaccion == -1 else 0

        # Guardar la encuesta usando función utils
        utils.hacer_encuesta(
            clase=materia_id,
            profesor=docente_id,
            ciclo=ciclo["id"],
            respuestas=respuestas,
            comentario=comentario,
            like=like,
            dislike=dislike
        )

        # Registrar que este estudiante ya realizó evaluación para evitar duplicados
        utils.registrar_evaluacion_realizada(estudiante["id"], docente_id, materia_id, ciclo["id"])

        return redirect("inicio_estudiante")

    return render(request, "estudiante/evaluacion.html", {
        "docente": docente["nombre"] if docente else "Desconocido",
        "materia": materia["nombre"] if materia else "Desconocida"
    })

def cerrar_sesion(request):
    Session.objects.all().delete()  # Elimina la sesión del usuario
    return redirect('/')  # Redirige al login u otra página


