import Turnero

profesionales = [
    ["1", "Perez, Carolina", "Cardiologia", 9, 17],
    ["2", "Gomez, Alejandra", "Clinica Medica", 8, 16],
    ["3", "Lopez, Eduardo", "Traumatologia", 10, 18] #incluimos profesionales de prueba
]

#para sacar el horario del profesional que se esta sacando turno, chequeamos con el id y evitamos reescribir.
def getHorarioProfesional(id):
    for profesional in profesionales:
        if profesional[0] == id:
            return str(profesional[3]) + " a " + str(profesional[4]) + " hs"
    return None

#para chequear si el profesional tiene turnos asignados, es util por ejemplo al momento de eliminar un profesional, primero chequear si tiene turnos
def tieneTurnos(id):
    if not Turnero.turnos:
        return False
    for turno in Turnero.turnos:
        if turno[1] == id:
            return True
    return False

def mostrarProfesionales():
    print("Los profesionales disponibles son: ")

    for profesional in profesionales:
        print(
            "Matricula: " + profesional[0] +
            ", Nombre: " + profesional[1] +
            ", Especialidad: " + profesional[2] +
            ", Horario: " + getHorarioProfesional(profesional[0])
        )

    return


def menu():
    eleccion = 0

    eleccion = int(input(
        "Gestión de profesionales, ingrese: \n"
        "1 para agregar un profesional. \n"
        "2 para quitar un profesional. \n"
        "3 para modificar un profesional. \n"
        "4 para modificar el horario de un profesional. \n"
    ))

    match eleccion:
        case 1:
            agregarProfesionales()
        case 2:
            quitarProfesionales()
        case 3:
            editarProfesionales()
        case 4:
            modificarHorario()
        case _:
            print("Opción incorrecta.")

    return


def modificarHorario():
    id = input("Ingrese ID del profesional: ")

    for profesional in profesionales:
        if profesional[0] == id:
            print(
                "Horario actual: " +
                getHorarioProfesional(profesional[0])
            )

            hInicio = input("Ingrese nuevo horario de comienzo de atencion: ")
            hFin = input("Ingrese nuevo horario de fin de atencion: ")

            profesional[3] = hInicio
            profesional[4] = hFin

            print("Horario modificado")
            return

    print("No se encontró un profesional con la matricula o ID ingresado")
    return


def editarProfesionales():
    mostrarProfesionales()

    id = input("Ingrese matricula o ID del profesional para editar: ")

    for profesional in profesionales:
        if profesional[0] == id:
            print("Nombre actual: " + profesional[1])

            nombre = input(
                "Ingrese nuevo nombre: o  enter para mantener el nombre actual: "
            )

            if nombre == "":
                nombre = profesional[1]

            print("Especialidad actual: " + profesional[2])

            especialidad = input(
                "Ingrese nueva especialidad: o bien presione enter "
                "para mantener la especialidad actual: "
            )

            if especialidad == "":
                especialidad = profesional[2]

            profesional[1] = nombre
            profesional[2] = especialidad

            print("Profesional  modificado")
            return

    print("No se encontró un profesional con la matricula o id ingresado")
    return


def agregarProfesionales():
    mostrarProfesionales()

    id = input("Ingrese matricula/id del profesional para agregar: ")
    nombre = input("Ingrese nombre del profesional: ")
    especialidad = input("Ingrese especialidad del profesional: ")
    hInicio = input(
        "Ingrese horario de comienzo de atencion: "
    )
    hFin = input(
        "Ingrese horario de fin de atencion: "
    )

    profesionales.append([
        id,
        nombre,
        especialidad,
        hInicio,
        hFin
    ])

    return


def quitarProfesionales():
    mostrarProfesionales()

    id = input("Ingrese matricula o ID del profesional a quitar: ")

    if tieneTurnos(id):
        print("No se puede eliminar el profesional porque tiene turnos asignados, cancele primero los turnos.")
        return

    for p in profesionales:
        if p[0] == id:
            profesionales.remove(p)
            print("eliminado")
            return

    print("No se encontró un profesional con la matricula / ID ingresado.")
    return
