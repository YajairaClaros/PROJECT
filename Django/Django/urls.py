"""
URL configuration for Django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import E_Docente.views as views

urlpatterns = [

    path('', views.index, name='index'),


    #Rutas vistas de admin
    path('admin/index', views.inicio_admin, name='inicio_admin'),
    path('admin/docentes', views.docentes, name='docentes'),
    path('admin/editar_docente/<int:docente_id>/', views.editar_docente, name='editar_docente'),
    path('admin/estudiantes', views.estudiantes, name='estudiantes'),
    path('admin/editar_estudiante/<int:id>/', views.editar_estudiante, name='editar_estudiante'),
    path('admin/materias', views.materias, name='materias'),
    path("admin/editar_materia/<int:id>/", views.editar_materia, name="editar_materia"),
    path('admin/resultados', views.resultados, name='resultados'),
    path('admin/detalles_resultado', views.detalles_resultado, name='d_resultado'),



    # Rutas vistas de estudiante
    path('estudiante/index', views.inicio_estudiante, name='inicio_estudiante'),
    path('estudiante/evaluacion', views.evaluacion, name='ev_estudiante'),
]
