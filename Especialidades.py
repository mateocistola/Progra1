
import json


ARCHIVO_ESPECIALIDADES = "especialidades.json"


def cargarEspecialidades():
    try:
        archivo = open(ARCHIVO_ESPECIALIDADES, "rt", encoding="utf-8")
        especialidades = json.load(archivo)
        archivo.close()

        if not isinstance(especialidades, list):
            raise ValueError("El archivo de especialidades debe contener una lista.")

        for especialidad in especialidades:
            if not isinstance(especialidad, str) or especialidad.strip() == "":
                raise ValueError("El archivo contiene especialidades inválidas.")

        return especialidades

    except FileNotFoundError:
        especialidades = [
            "Cardiología",
            "Clínica Médica",
            "Traumatología"
        ]
        guardarEspecialidades(especialidades)
        return especialidades

    except (OSError, json.JSONDecodeError, ValueError) as mensaje:
        print("No se pudieron cargar las especialidades:", mensaje)
        return []


def guardarEspecialidades(especialidades):
    archivo = None
    guardado = False

    try:
        archivo = open(ARCHIVO_ESPECIALIDADES, "wt", encoding="utf-8")
        json.dump(especialidades, archivo, ensure_ascii=False, indent=4)
        guardado = True

    except OSError as mensaje:
        print("No se pudieron guardar las especialidades:", mensaje)

    finally:
        if archivo is not None:
            archivo.close()

    return guardado


# Busca una especialidad utilizando recursividad.
# Devuelve su posición o -1 si no existe.
def buscarPosicionEspecialidad(especialidades, nombre, posicion=0):
    if posicion >= len(especialidades):
        return -1

    if especialidades[posicion].lower() == nombre.lower():
        return posicion

    return buscarPosicionEspecialidad(especialidades, nombre, posicion + 1)


def especialidadRegistrada(especialidades, nombre):
    posicion = buscarPosicionEspecialidad(especialidades, nombre)
    return posicion != -1


def listarEspecialidades(especialidades):
    if not especialidades:
        print("No hay especialidades registradas")
    else:
        print("Especialidades registradas:")

        for posicion in range(len(especialidades)):
            print(str(posicion + 1) + ". " + especialidades[posicion])


def agregarEspecialidad(especialidades):
    nombre = input("Ingrese el nombre de la especialidad: ").strip()

    while nombre == "":
        print("El nombre no puede estar vacío")
        nombre = input("Ingrese nuevamente el nombre de la especialidad: ").strip()

    if especialidadRegistrada(especialidades, nombre):
        print("La especialidad ya está registrada")
        return False

    especialidades.append(nombre)
    print("Especialidad registrada correctamente")
    return True


def modificarEspecialidad(especialidades):
    if not especialidades:
        print("No hay especialidades registradas")
        return False

    listarEspecialidades(especialidades)

    nombreActual = input(
        "Ingrese el nombre de la especialidad que desea cambiar: "
    ).strip()

    posicion = buscarPosicionEspecialidad(especialidades, nombreActual)

    if posicion == -1:
        print("No se encontró la especialidad ingresada")
        return False

    nombreNuevo = input("Ingrese el nuevo nombre de la especialidad: ").strip()

    while nombreNuevo == "":
        print("El nombre no puede estar vacío")
        nombreNuevo = input("Ingrese nuevamente el nombre: ").strip()

    if (especialidadRegistrada(especialidades, nombreNuevo)
            and nombreNuevo.lower() != especialidades[posicion].lower()):
        print("Ya existe otra especialidad con ese nombre")
        return False

    especialidadAnterior = especialidades[posicion]

    # Se actualizan primero los profesionales para evitar cambiar el JSON
    # si no se pudo reescribir el archivo de profesionales.
    import Profesionales

    if not Profesionales.actualizarEspecialidadProfesionales(
            especialidadAnterior, nombreNuevo):
        print("No se pudo actualizar la especialidad en los profesionales.")
        return False

    especialidades[posicion] = nombreNuevo
    print("Especialidad modificada correctamente")
    return True


def especialidadAsignada(nombre):
    import Profesionales
    return Profesionales.existeProfesionalPorEspecialidad(nombre)


def quitarEspecialidad(especialidades):
    if not especialidades:
        print("No hay especialidades registradas")
        return False

    listarEspecialidades(especialidades)

    nombre = input(
        "Ingrese el nombre de la especialidad que desea eliminar: "
    ).strip()

    posicion = buscarPosicionEspecialidad(especialidades, nombre)

    if posicion == -1:
        print("No se encontró la especialidad ingresada")
        return False

    especialidadEncontrada = especialidades[posicion]

    if especialidadAsignada(especialidadEncontrada):
        print("No se puede eliminar la especialidad porque está asignada a uno o más profesionales")
        return False

    especialidades.pop(posicion)
    print("Especialidad eliminada correctamente")
    return True


def menu():
    eleccion = 0

    while eleccion != 5:
        eleccion = input(
            "Gestión de especialidad, ingrese: \n"
            "1 para agregar una especialidad. \n"
            "2 para listar las especialidades. \n"
            "3 para modificar una especialidad. \n"
            "4 para eliminar una especialidad. \n"
            "5 para volver al menú principal. \n"
        )

        while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > 5:
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre el 1 y 5: ")

        eleccion = int(eleccion)
        especialidades = cargarEspecialidades()

        match eleccion:
            case 1:
                cambio = agregarEspecialidad(especialidades)
                if cambio:
                    guardarEspecialidades(especialidades)

            case 2:
                listarEspecialidades(especialidades)

            case 3:
                cambio = modificarEspecialidad(especialidades)
                if cambio:
                    guardarEspecialidades(especialidades)

            case 4:
                cambio = quitarEspecialidad(especialidades)
                if cambio:
                    guardarEspecialidades(especialidades)

            case 5:
                print("Volviendo al menú principal")

