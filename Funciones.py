import json as js

# Devuelve un diccionario copiado del json de datos.
def get():
    with open ("D:\KEY Institute\MATERIAS\SEMESTRE I\FUNDAMENTOS DE PROGRAMACIÓN\Proyecto final\PROJECT\datos.json", "r") as file:
        data = js.load(file)

    return data

# Reescribe los cambios realizados al archivo de base de datos.
def rewrite(cambios):
    with open("D:\KEY Institute\MATERIAS\SEMESTRE I\FUNDAMENTOS DE PROGRAMACIÓN\Proyecto final\PROJECT\datos.json", "w") as file:
        js.dump(cambios, file, indent=4)

    return None

# Crea un usuario en la base datos, asignando un nombre, una contraseña y un tipo (estudiante o administrador).
def crear_usuario(cuenta, password, tipo):

    data = get()
    usuarios = data[0]

    if cuenta_ya_existe(cuenta) == True:
         #Hola @Dennis, no sé qué ponerle a este mensaje, supongo que eso lo vemos después con la interfaz, este print se puede cambiar xd.
        print("La cuenta ya existe mi broda")
        return None
    else:
        id = "usuario"+str(len(usuarios))
        usuarios[id] = {"cuenta": cuenta, "password": password, "tipo": tipo}
        rewrite(data)

    return None

# Devuelve True si una cuenta ya existe, de lo contrario devuelve False.
def cuenta_ya_existe(cuenta):
    
    data = get()
    usuarios = data[0]

    for usuario in usuarios:
        if cuenta == usuarios[usuario]["cuenta"]:
            return True
    
    return False

# Agrega una materia a la base de datos, y asigna una lista vacía donde irán los profesores de dicha materia.
def agregar_materia(materia):
    
    data = get()
    materias = data[1]

    if materia_ya_existe(materia) == True:
        print("la materia ya existe mi broda")
        return None
    else:
        materias[materia] = []

    rewrite(data)

    return None

# Devuelve True si una materia ya existe, de lo contrario devuelve False.
def materia_ya_existe(materia):

    data = get()
    materias = data[1]

    for opcion in materias:
        if materia == opcion:
            return True
    
    return False

# Devuelve True si un profesor ya existe, de lo contrario devuelve False.
def profe_ya_existe(profesor):

    data = get()
    materias = data[1]

    for materia in materias:
        if profesor in materias[materia]:
            return True
        
    return False

# Agrega un profesor asignado a una materia a la base de datos.
def agregar_profesor(profesor, materia):
    
    data = get()
    materias = data[1]

    if profe_ya_existe(profesor) == True:
        print("El profe ya existe mi broda")
        return None

    for opcion in materias:
        if materia == opcion:
            materias[opcion].append(profesor)
            rewrite(data)
            return None
    
    print("la materia no existe mi broda")
    return None

# Guarda el resultado de una encuesta en la base de datos.
# Importante cuidar las clases de cada una de las variables para esta función.
def hacer_encuesta(usuario, clase, profesor, nota, comentario, like, dislike):

    data = get()
    
    entry = len(data)-2

    encuesta = {"entry": entry, "usuario": usuario, "clase": clase, "profesor": profesor, "nota": nota, "comentario": comentario, "like": like, "dislike": dislike}

    data.append(encuesta)

    rewrite(data)

    return None

# Devuelve True si se logra un loggeo correcto (nombre correcto y contraseña correcta), de lo contrario devuelve False.
def login(nombre, contra):

    data = get()
    usuarios = data[0]

    for usuario in usuarios:
        if usuarios[usuario]["cuenta"] == nombre:
                if usuarios[usuario]["password"] == contra:
                    return True
    
    return False
 
# Elimina una materia del diccionario de materias en la base de datos.
def eliminar_materia(materia):

    data = get()
    materias = data[1]

    materias.pop(materia)

    rewrite(data)

    return None

# Elimina un profesor de la lista de profesores asignados a una materia en la base de datos.
def eliminar_profesor(profesor):

    data = get()
    materias = data[1]

    for materia in materias:
        if profesor in materias[materia]:
            materias[materia].remove(profesor)

    rewrite(data)
    
    return None

# Devuelve True si un usuario pertenece al tipo "administrador".
def es_admin(nombre):
    
    data = get()
    usuarios = data[0]

    for usuario in usuarios:
        if usuarios[usuario]["cuenta"] == nombre:
            if usuarios[usuario]["tipo"] == 1:
                return True
            
    return False