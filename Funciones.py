import json as js

def get():
    with open ("D:\KEY Institute\MATERIAS\SEMESTRE I\FUNDAMENTOS DE PROGRAMACIÓN\Proyecto final\PROJECT\datos.json", "r") as file:
        data = js.load(file)

    return data

def rewrite(cambios):
    with open("D:\KEY Institute\MATERIAS\SEMESTRE I\FUNDAMENTOS DE PROGRAMACIÓN\Proyecto final\PROJECT\datos.json", "w") as file:
        js.dump(cambios, file, indent=4)

    return None

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

def cuenta_ya_existe(cuenta):
    
    data = get()
    usuarios = data[0]

    for usuario in usuarios:
        if cuenta == usuarios[usuario]["cuenta"]:
            return True
    
    return False

def guardar_encuesta(encuesta):


    data = get()
    data.append(encuesta)

    rewrite(data)

    return None

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

def materia_ya_existe(materia):

    data = get()
    materias = data[1]

    for opcion in materias:
        if materia == opcion:
            return True
    
    return False

def profe_ya_existe(profesor):

    data = get()
    materias = data[1]

    for materia in materias:
        if profesor in materias[materia]:
            return True
        
    return False

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

# Importante cuidar las clases de cada una de las variables para esta función:
def hacer_encuesta(usuario, clase, profesor, nota, comentario, like, dislike):

    data = get()
    
    entry = len(data)-2

    encuesta = {"entry": entry, "usuario": usuario, "clase": clase, "profesor": profesor, "nota": nota, "comentario": comentario, "like": like, "dislike": dislike}

    data.append(encuesta)

    rewrite(data)

    return None

# SIN TERMINAR:
def login(nombre, contra):

    data = get()
    usuarios = data[0]

    for usuario in usuarios:
        if usuarios[usuario]["cuenta"] == nombre:
                if usuarios[usuario]["password"] == contra:
                    return True
    
    return False
 
def eliminar_materia(materia):

    data = get()
    materias = data[1]

    materias.pop(materia)

    rewrite(data)

    return None

def eliminar_profesor(profesor):

    data = get()
    materias = data[1]

    for materia in materias:
        if profesor in materias[materia]:
            materias[materia].remove(profesor)

    rewrite(data)
    
    return None

agregar_profesor("Regina Serpas", "introalaing")