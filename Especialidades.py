#Comprueba si una especialidad ya está registrada

def especialidadRegistrada(especialidades, nombre):
    registrada = False

    for especialidad in especialidades:
        #Convertimos ambos nombres a minúsculas para comparar sin distinguir entre mayúsculas y minúsculas
        if especialidad.lower() == nombre.lower():
            registrada = True

    return registrada


#Muestra todas las especialidades registradas.

def listarEspecialidades(especialidades):
    if not especialidades:
        print("No hay especialidades registradas")
    else:
        print("Ya hay especialidades registradas")

        for posicion in range(len(especialidades)):
            print(str(posicion + 1) + ". " + especialidades[posicion])


#Agrega una especialidad si el nombre no está vacío y todavía no se encuentra registrado.

def agregarEspecialidad(especialidades):
    nombre = input("Ingrese el nombre de la especialidad: ")

    while nombre == "":
        print("El nombre no puede estar vacío")
        nombre = input("Ingrese nuevamente el nombre de la especialidad: ")

    if especialidadRegistrada(especialidades, nombre):
        print("La especialidad ya está registrada")
    else:
        especialidades.append(nombre)
        print("Especialidad registrada correctamente")

#Modifica una especialidad y actualiza a los profesionales que la tengan asignada

def modificarEspecialidad(especialidades, profesionales):
    if not especialidades:
        print("No hay especialidades registradas")
        return

    listarEspecialidades(especialidades)

    nombreActual = input("Ingrese el nombre de la especialidad que desea cambiar: ")

    especialidadEncontrada = ""

    for especialidad in especialidades:
        if especialidad.lower() == nombreActual.lower():
            especialidadEncontrada = especialidad

    if especialidadEncontrada == "":
        print("No se encontró la especialidad ingresada")
    else:
        nombreNuevo = input("Ingrese el nuevo nombre de la especialidad: ")

        while nombreNuevo == "":
            print("El nombre no puede estar vacío")
            nombreNuevo = input("Ingrese nuevamente el nombre: ")

        if (especialidadRegistrada(especialidades, nombreNuevo) and nombreNuevo.lower() != especialidadEncontrada.lower()):
            print("Ya existe otra especialidad con ese nombre")
        else:
            #Modificamos el nombre de la lista de especialidades
            for posicion in range(len(especialidades)):
                if(especialidades[posicion].lower() == especialidadEncontrada.lower()):
                    especialidades[posicion] = nombreNuevo

            #Actualizamos también a los profesionales que tenían asignada la especialidad anterior.
            for profesional in profesionales:
                if(profesional[2].lower() == especialidadEncontrada.lower()):
                    profesional[2] = nombreNuevo

            print("Especialidad modificada correctamente")


#Comprobar si una especialidad está asignada a algún profesional

def especialidadAsignada(profesionales, nombre):
    asignada = False
    for profesional in profesionales:
        if profesional[2].lower() == nombre.lower():
            asignada = True

    return asignada

#Elimina una especialidad si no está asignada a ningún profesional
def quitarEspecialidad(especialidades, profesionales):
    if not especialidades:
        print("No hay especialidades registradas")
        return

    listarEspecialidades(especialidades)

    nombre = input("Ingrese el nombre de la especialidad que desea eliminar: ")
    especialidadEncontrada = ""
    for especialidad in especialidades:
        if especialidad.lower() == nombre.lower():
            especialidadEncontrada = especialidad
    if especialidadEncontrada == "":
        print("No se encontró la especialidad ingresada")

    elif especialidadAsignada(profesionales, especialidadEncontrada):
        print("No se puede eliminar la especialidad porque está asignada a uno o más profesionales")
    else:
        especialidades.remove(especialidadEncontrada)
        print("Especialidad eliminada correctamente")