from django.shortcuts import render, redirect
from . import utils


# Create your views here.
def index(request):
    if request.method == "POST":
        cuenta = request.POST.get("cuenta")
        password = request.POST.get("password")
        if utils.login(cuenta, password):
            request.session["usuario"] = cuenta
            if utils.es_admin(cuenta):
                return redirect("inicio_admin")  # Ruta para admin
            else:
                return redirect("inicio_estudiante")  # Ruta para estudiante
        else:
           return render(request, "index.html", {"error": "Usuario o contraseña incorrecta"})

    return render(request, "index.html")

#Vistas de admin
def inicio_admin(request):
    return render(request, 'admin/index.html')

def docentes(request):
    return render(request, 'admin/docentes.html')

def editar_docente(request):
      return render(request, 'admin/editar_docente.html')

def estudiantes(request):
    return render(request, 'admin/estudiantes.html')

def editar_estudiante(request):
    return render(request, 'admin/editar_estudiante.html')

def materias(request):
    return render(request, 'admin/materias.html')

def editar_materia(request):
    return render(request, 'admin/editar_materias.html')

def resultados(request):
    return render(request, 'admin/resultados.html')

def detalles_resultado(request):
    return render(request, 'admin/detalles_resultados.html')



#Vistas de estudiante
def inicio_estudiante(request):
    return render(request, 'estudiante/index.html')

def evaluacion(request):
    return render(request, 'estudiante/evaluacion.html')