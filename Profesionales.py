
#para sacar el horario del profesional que se esta sacando turno, chequeamos con el id y evitamos reescribir.
def getHorarioProfesional(profesionales, legajo):
    horario = None

    for profesional in profesionales:
        if profesional[0] == legajo:
            horario = str(profesional[3]) + " a " + str(profesional[4]) + " hs"
    return horario

#para chequear si el profesional tiene turnos asignados, es util por ejemplo al momento de eliminar un profesional, primero chequear si tiene turnos
def tieneTurnos(turnos, legajo):
    tieneTurnosAsignados = False

    for turno in turnos:
        if turno[1] == legajo:
            tieneTurnosAsignados = True
    return tieneTurnosAsignados

def mostrarProfesionales(profesionales):
    print("Los profesionales disponibles son: ")

    for profesional in profesionales:
        print(
            "Legajo: " + profesional[0] +
            ", Nombre: " + profesional[1] +
            ", Especialidad: " + profesional[2] +
            ", Horario: " + getHorarioProfesional(profesionales, profesional[0])
        )




def menu(profesionales, turnos):


    eleccion = int(input(
        "Gestión de profesionales, ingrese: \n"
        "1 para agregar un profesional. \n"
        "2 para quitar un profesional. \n"
        "3 para modificar un profesional. \n"
        "4 para modificar el horario de un profesional. \n"
        "5 para salir. \n"
    ))

    match eleccion:
        case 1:
            agregarProfesionales(profesionales)
        case 2:
            quitarProfesionales(profesionales, turnos)
        case 3:
            editarProfesionales(profesionales)
        case 4:
            modificarHorario(profesionales)
        case 5:
            print("Volvemos al menú principal")
        case _:
            print("Opción incorrecta.")

   


def modificarHorario(profesionales):
    legajo = input("Ingrese el legajo del profesional: ")

    profesionalEncontrado = []

    for profesional in profesionales:
        if profesional[0] == legajo:
            profesionalEncontrado = profesional

    if profesionalEncontrado:
        print(
              "Horario actual: " +
              getHorarioProfesional(profesionales, legajo)
        )

        horaInicio = input("Ingrese nuevo horario de comienzo de atencion: ")
        horaFin = input("Ingrese nuevo horario de fin de atencion: ")

        profesionalEncontrado[3] = horaInicio
        profesionalEncontrado[4] = horaFin

        print("Horario modificado")
    else:
        print("No se encontró un profesional con el legajo ingresado")



def editarProfesionales(profesionales):
    mostrarProfesionales(profesionales)

    legajo = input("Ingrese legajo del profesional para editar: ")

    profesionalEncontrado = []

    for profesional in profesionales:
        if profesional[0] == legajo:
            profesionalEncontrado = profesional

    if profesionalEncontrado:
       print("Nombre actual: " + profesionalEncontrado[1])

       nombre = input(
            "Ingrese nuevo nombre: o  enter para mantener el nombre actual: "
       )

       if nombre == "":
            nombre = profesionalEncontrado[1]

       print("Especialidad actual: " + profesionalEncontrado[2])

       especialidad = input(
                "Ingrese nueva especialidad: o bien presione enter "
                "para mantener la especialidad actual: "
       )

       if especialidad == "":
            especialidad = profesionalEncontrado[2]

       profesionalEncontrado[1] = nombre
       profesionalEncontrado[2] = especialidad

       print("Profesional  modificado")
    else:

       print("No se encontró un profesional con el legajo ingresado")



def agregarProfesionales(profesionales):
    mostrarProfesionales(profesionales)

    legajo = input("Ingrese legajo del profesional para agregar: ")
    nombre = input("Ingrese nombre del profesional: ")
    especialidad = input("Ingrese especialidad del profesional: ")
    horaInicio = input(
        "Ingrese horario de comienzo de atencion: "
    )
    horaFin = input(
        "Ingrese horario de fin de atencion: "
    )

    profesionales.append([
        legajo,
        nombre,
        especialidad,
        horaInicio,
        horaFin
    ])

    print("Profesional agregado correctamente")


def quitarProfesionales(profesionales, turnos):
    mostrarProfesionales(profesionales)

    legajo = input("Ingrese el legajo del profesional a quitar: ")

    if tieneTurnos(turnos, legajo):
        print("No se puede eliminar el profesional porque tiene turnos asignados, cancele primero los turnos.")

    else:
        profesionalesEliminar = []

        for profesional in profesionales:
            if profesional[0] == legajo:
                profesionalesEliminar = profesional

        if profesionalesEliminar:
            profesionales.remove(profesionalesEliminar)
            print("Profesional eliminado")
        else:

            print("No se encontró un profesional con el legajo ingresado.")

