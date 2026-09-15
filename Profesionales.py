profesionales = [
    ["1", "Perez, Carolina", "Cardiologia", 9, 17],
    ["2", "Gomez, Alejandra", "Clinica Medica", 8, 16],
    ["3", "Lopez, Eduardo", "Traumatologia", 10, 18]
]


def mostrarProfesionales():
    print("Los profesionales disponibles son: ")

    for profesional in profesionales:
        print(
            "Matricula: " + profesional[0] +
            ", Nombre: " + profesional[1] +
            ", Especialidad: " + profesional[2] +
            ", Horario: " + str(profesional[3]) +
            " - " + str(profesional[4])
        )

    return


def menu():
    eleccion = 0

    eleccion = int(input(
        "Ingrese 1 para agregar un profesional, "
        "2 para quitar un profesional, "
        "3 para modificar un profesional, "
        "4 para modificar el horario de un profesional: "
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
            print("Opción inválida.")

    return


def modificarHorario():
    id = input("Ingrese ID del profesional: ")

    for profesional in profesionales:
        if profesional[0] == id:
            print(
                "Horario actual: " +
                str(profesional[3]) +
                " - " +
                str(profesional[4])
            )

            hInicio = input("Ingrese nuevo horario comienzo de atencion: ")
            hFin = input("Ingrese nuevo horario fin de atencion: ")

            profesional[3] = hInicio
            profesional[4] = hFin

            print("Horario modificado")
            return

    print("No se encontró un profesional con el ID ingresado")
    return


def editarProfesionales():
    mostrarProfesionales()

    id = input("Ingrese ID del profesional para editar: ")

    for profesional in profesionales:
        if profesional[0] == id:
            print("Nombre actual: " + profesional[1])

            nombre = input(
                "Ingrese nuevo nombre: o bien presione enter "
                "para mantener el nombre actual: "
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

            print("Profesional modificado")
            return

    print("No se encontró un profesional con el ID ingresado")
    return


def agregarProfesionales():
    mostrarProfesionales()

    id = input("Ingrese ID del profesional a agregar: ")
    nombre = input("Ingrese nombre del profesional: ")
    especialidad = input("Ingrese especialidad del profesional: ")
    hInicio = input(
        "Ingrese horario comienzo de atencion del del profesional: "
    )
    hFin = input(
        "Ingrese horario fin de atencion del del profesional: "
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

    id = input("Ingrese ID del profesional a quitar: ")

    for p in profesionales:
        if p[0] == id:
            profesionales.remove(p)
            print("Profesional eliminado")
            return

    print("No se encontró un profesional con el ID ingresado")
    return