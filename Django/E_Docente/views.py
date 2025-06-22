from django.shortcuts import render, redirect
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
    return render(request, 'admin/docentes.html')


def editar_docente(request):
    return render(request, 'admin/editar_docente.html')


def estudiantes(request):
    error = None
    if request.method == "POST":
        nombre = request.POST.get("name")
        cuenta = request.POST.get("cuenta")
        password = request.POST.get("password")

        if utils.cuenta_ya_existe(cuenta):
            error = "La cuenta ya existe, elige otro nombre de usuario."
        else:
            utils.crear_usuario(cuenta, password, 0, nombre)
            return redirect("estudiantes")

    data = utils.get()
    estudiantes = [u for u in data["usuarios"] if u["tipo"] == 0]
    materias_dict = {m["id"]: m["nombre"] for m in data["materias"]}

    for e in estudiantes:
        e["materias_nombres"] = [materias_dict.get(mid, "Desconocida") for mid in e["materias"]]

    return render(request, 'admin/estudiantes.html', {
        "estudiantes": estudiantes,
        "error": error,
    })




def editar_estudiante(request, id):
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
    return render(request, 'admin/materias.html')


def editar_materia(request):
    return render(request, 'admin/editar_materias.html')


def resultados(request):
    return render(request, 'admin/resultados.html')


def detalles_resultado(request):
    return render(request, 'admin/detalles_resultados.html')


# Vistas de estudiante
def inicio_estudiante(request):
    return render(request, 'estudiante/index.html')


def evaluacion(request):
    return render(request, 'estudiante/evaluacion.html')
