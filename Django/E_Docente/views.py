from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import utils


# Create your views here.
def index(request):
    if request.method == "POST":  # -------------------------------> INICIO DE SESIÓN
        cuenta = request.POST.get("cuenta")
        password = request.POST.get("password")
        if utils.login(cuenta, password):  # --------------> Verificar si el usuario o contraseña incorrecta
            request.session["usuario"] = cuenta
            if utils.es_admin(cuenta):  # ----------> Verificar si es admin

                return redirect("inicio_admin")  # Ruta para admin
            else:
                return redirect("inicio_estudiante")  # Ruta para estudiante
        else:
            return render(request, "index.html", {"error": "Usuario o contraseña incorrecta"})

    return render(request, "index.html")


# Vistas de admin
def inicio_admin(request):
    if "usuario" not in request.session:
        return redirect("/")

    if request.method == "POST":
        try:
            id = int(request.POST.get("id"))
            estado = int(request.POST.get("estado"))
            utils.cambiar_estado_evaluacion(id, estado)


        except Exception as e:
            return render(request, 'admin/index.html', {
                'ciclo': utils.obtener_ciclo_activo(),
                'error': 'No se ha podido modificar el estado de la evaluación'
            })

    ciclo = utils.obtener_ciclo_activo()
    return render(request, 'admin/index.html', {'ciclo': ciclo})



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

        if utils.profe_ya_existe(nombre):
            error = "El docente ya existe."
        else:
            utils.agregar_profesor(nombre)

            # Vuelve a buscar el ID recién agregado
            nuevo_docente = next((d for d in utils.get()["docentes"] if d["nombre"] == nombre), None)

            if nuevo_docente and materia_id:
                utils.asignar_materia_a_profesor(nuevo_docente["id"], int(materia_id))

        return redirect("docentes")

    # Agregar nombres de materias a cada docente
    for docente in docentes:
        docente["materias_nombres"] = [
            mat["nombre"] for mat in materias if mat["id"] in docente["materias"]
        ]

    return render(request, "admin/docentes.html", {
        "docentes": docentes,
        "materias": materias,
        "error": error
    })


def editar_docente(request, docente_id):

    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()
    docentes = data["docentes"]
    materias = data["materias"]

    docente = next((d for d in docentes if d["id"] == docente_id), None)
    if not docente:
        return redirect("docentes")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "actualizar":
            docente["nombre"] = request.POST.get("name")
            docente["estado"] = int(request.POST.get("estado"))
            utils.rewrite(data)
            return redirect("docentes")

        elif action == "agregar_materia":
            materia_id = int(request.POST.get("subject"))
            utils.asignar_materia_a_profesor(docente_id, materia_id)
            return redirect("editar_docente", docente_id=docente_id)

        elif action == "quitar_materia":
            materia_id = int(request.POST.get("materia_id"))
            if materia_id in docente["materias"]:
                docente["materias"].remove(materia_id)
            for materia in materias:
                if materia_id == materia["id"] and docente_id in materia["docentes"]:
                    materia["docentes"].remove(docente_id)
            utils.rewrite(data)
            return redirect("editar_docente", docente_id=docente_id)

    materias_asignadas = [
        mat for mat in materias if mat["id"] in docente["materias"]
    ]
    materias_disponibles = [
        mat for mat in materias if mat["id"] not in docente["materias"]
    ]

    return render(request, "admin/editar_docente.html", {
        "docente": docente,
        "materias_asignadas": materias_asignadas,
        "materias": materias_disponibles,
    })


def estudiantes(request):
    if "usuario" not in request.session:
        return redirect("/")

    if "usuario" not in request.session:
        return redirect("/")



    error = None  # Variable para almacenar posibles mensajes de error

    if request.method == "POST":
        # Obtener datos enviados por el formulario
        nombre = request.POST.get("name")
        cuenta = request.POST.get("cuenta")
        password = request.POST.get("password")

        # Verificar si la cuenta ya existe para evitar duplicados
        if utils.cuenta_ya_existe(cuenta):
            error = "La cuenta ya existe, elige otro nombre de usuario."
        else:
            # Crear nuevo usuario de tipo estudiante (tipo=0)
            utils.crear_usuario(cuenta, password, 0, nombre)
            # Redirigir para recargar la lista de estudiantes
            return redirect("estudiantes")

    # Si no es POST o hubo error, cargar datos actuales
    data = utils.get()
    # Filtrar solo usuarios que son estudiantes (tipo=0)
    estudiantes = [u for u in data["usuarios"] if u["tipo"] == 0]
    # Crear un diccionario para mapear id de materia a nombre
    materias_dict = {m["id"]: m["nombre"] for m in data["materias"]}

    # Para cada estudiante, agregar una lista con los nombres de las materias asignadas
    for e in estudiantes:
        e["materias_nombres"] = [materias_dict.get(mid, "Desconocida") for mid in e["materias"]]

    # Renderizar la plantilla pasando estudiantes y posible mensaje de error
    return render(request, 'admin/estudiantes.html', {
        "estudiantes": estudiantes,
        "error": error,
    })


def editar_estudiante(request, id):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()  # Carga el contenido actual de la base de datos (JSON)
    estudiante = next((u for u in data["usuarios"] if u["id"] == id), None)  # Busca el estudiante por ID
    materias = data["materias"]  # Lista de materias disponibles

    if not estudiante:
        return redirect("estudiantes")  # Redirige si no se encontró el estudiante

    if request.method == "POST":
        action = request.POST.get("action")  # Determina la acción a realizar (actualizar, agregar o quitar)

        if action == "actualizar":
            # Actualiza los datos básicos del estudiante
            estudiante["nombre"] = request.POST.get("name")
            estudiante["cuenta"] = request.POST.get("cuenta")
            estudiante["password"] = request.POST.get("password")
            estudiante["estado"] = int(request.POST.get("estado"))

        elif action == "agregar_materia":
            # Agrega una materia al estudiante si no la tiene
            materia_id = request.POST.get("subject")
            if materia_id and materia_id.isdigit():
                materia_id = int(materia_id)
                if materia_id not in estudiante["materias"]:
                    estudiante["materias"].append(materia_id)
                    for m in materias:
                        if m["id"] == materia_id and estudiante["id"] not in m["estudiantes"]:
                            m["estudiantes"].append(estudiante["id"])
                            break

        elif action == "quitar_materia":
            # Elimina una materia del estudiante si la tiene
            materia_id = int(request.POST.get("materia_id"))
            if materia_id in estudiante["materias"]:
                estudiante["materias"].remove(materia_id)
                for m in materias:
                    if m["id"] == materia_id and estudiante["id"] in m["estudiantes"]:
                        m["estudiantes"].remove(estudiante["id"])
                        break

        utils.rewrite(data)  # Guarda los cambios en el JSON
        return redirect("editar_estudiante", id=id)  # Recarga la misma vista

    # Materias que ya tiene asignadas el estudiante (para mostrarlas en la tabla)
    materias_asignadas = [m for m in materias if m["id"] in estudiante["materias"]]

    # Renderiza la plantilla con la información necesaria
    return render(request, "admin/editar_estudiante.html", {
        "estudiante": estudiante,
        "materias": materias,
        "materias_asignadas": materias_asignadas,
    })


def materias(request):
    if "usuario" not in request.session:
        return redirect("/")

    error = None

    if request.method == "POST":
        nombre = request.POST.get("name")
        codigo = request.POST.get("codigo")

        if utils.materia_ya_existe(codigo):
            error = "La materia ya existe."
        else:
            utils.agregar_materia(codigo, nombre)

        return redirect("materias")  # Evita reenvío del formulario

    data = utils.get()
    materias = data["materias"]
    docentes = data["docentes"]

    # Añadir nombres de docentes a cada materia
    for mat in materias:
        mat["docentes_nombres"] = [doc["nombre"] for doc in docentes if doc["id"] in mat["docentes"]]

    return render(request, "admin/materias.html", {
        "materias": materias,
        "docentes": docentes,
        "error": error
    })


def editar_materia(request, id):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()
    materias = data["materias"]
    docentes = data["docentes"]

    materia = next((m for m in materias if m["id"] == id), None)
    if not materia:
        return redirect("materias")  # Si no existe

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "actualizar":
            materia["nombre"] = request.POST.get("nombre")
            materia["codigo"] = request.POST.get("codigo")
            materia["estado"] = int(request.POST.get("estado"))
            utils.rewrite(data)
            return redirect("materias")

        elif action == "agregar_docente":
            docente_id = int(request.POST.get("docente_id"))
            utils.asignar_materia_a_profesor(docente_id, id)
            return redirect("editar_materia", id=id)

        elif action == "quitar_docente":
            docente_id = int(request.POST.get("docente_id"))
            if docente_id in materia["docentes"]:
                materia["docentes"].remove(docente_id)
                for doc in docentes:
                    if doc["id"] == docente_id and id in doc["materias"]:
                        doc["materias"].remove(id)
                utils.rewrite(data)
            return redirect("editar_materia", id=id)

    docentes_asignados = [doc for doc in docentes if doc["id"] in materia["docentes"]]
    docentes_disponibles = [doc for doc in docentes if doc["id"] not in materia["docentes"]]

    return render(request, "admin/editar_materia.html", {
        "materia": materia,
        "docentes_asignados": docentes_asignados,
        "docentes_disponibles": docentes_disponibles
    })



def resultados(request):
    if "usuario" not in request.session:
        return redirect("/")

    return render(request, 'admin/resultados.html')


def detalles_resultado(request):
    if "usuario" not in request.session:
        return redirect("/")

    return render(request, 'admin/detalles_resultados.html')


# Vistas de estudiante
def inicio_estudiante(request):
    if "usuario" not in request.session:
        return redirect("/")

    cuenta = request.session["usuario"]

    data = utils.get()
    usuarios = data["usuarios"]
    materias = data["materias"]
    docentes = data["docentes"]

    # Buscar al estudiante
    estudiante = next((u for u in usuarios if u["cuenta"] == cuenta and u["tipo"] == 0), None)
    if not estudiante:
        return redirect("login")

    ciclo = utils.obtener_ciclo_activo()
    evaluados = utils.obtener_docentes_evaluados(estudiante["id"], ciclo["id"])

    evaluables = []
    for mat_id in estudiante["materias"]:
        materia = next((m for m in materias if m["id"] == mat_id), None)
        if not materia:
            continue

        for docente_id in materia["docentes"]:
            docente = next((d for d in docentes if d["id"] == docente_id), None)
            if not docente:
                continue

            ya_evaluado = docente_id in evaluados
            evaluables.append({
                "docente": docente["nombre"],
                "materia": materia["nombre"],
                "evaluado": ya_evaluado,
                "materia_id": materia["id"],
                "docente_id": docente["id"]
            })


    return render(request, 'estudiante/index.html', {"evaluables": evaluables,"ciclo": ciclo})


def evaluacion(request, materia_id, docente_id):
    if "usuario" not in request.session:
        return redirect("/")

    data = utils.get()

    # Buscar estudiante
    cuenta = request.session["usuario"]
    estudiante = next((u for u in data["usuarios"] if u["cuenta"] == cuenta and u["tipo"] == 0), None)
    if not estudiante:
        return redirect("inicio_estudiante")

    ciclo = utils.obtener_ciclo_activo()
    materia = next((m for m in data["materias"] if m["id"] == materia_id), None)
    docente = next((d for d in data["docentes"] if d["id"] == docente_id), None)

    if request.method == "POST":
        respuestas = {
            f"pregunta{i}": int(request.POST.get(f"pregunta{i}", 0))
            for i in range(1, 21)
            if f"pregunta{i}" in request.POST
        }
        comentario = request.POST.get("comentario", "")
        reaccion = int(request.POST.get("like_dislike", 0))
        like = 1 if reaccion == 1 else 0
        dislike = 1 if reaccion == -1 else 0

        utils.hacer_encuesta(
            clase=materia_id,
            profesor=docente_id,
            ciclo=ciclo["id"],
            respuestas=respuestas,
            comentario=comentario,
            like=like,
            dislike=dislike
        )

        utils.registrar_evaluacion_realizada(estudiante["id"], docente_id, materia_id, ciclo["id"])
        return redirect("inicio_estudiante")

    return render(request, "estudiante/evaluacion.html", {
        "docente": docente["nombre"] if docente else "Desconocido",
        "materia": materia["nombre"] if materia else "Desconocida"
    })
