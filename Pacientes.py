
import os


ARCHIVO_PACIENTES = "pacientes.txt"
ARCHIVO_AUXILIAR = "pacientes_aux.txt"


def validarDni(dni):
    return (len(dni) == 7 or len(dni) == 8) and dni.isdigit()


def pedirDni(mensaje):
    dni = input(mensaje)

    while not validarDni(dni):
        print("DNI no válido. Debe contener 7 u 8 números.")
        dni = input(mensaje)

    return dni


def validarTexto(texto):
    return texto != "" and ";" not in texto and "\n" not in texto


def buscarPacientePorDNI(dni):
    archivo = None
    pacienteEncontrado = None

    try:
        archivo = open(ARCHIVO_PACIENTES, "rt", encoding="utf-8")
        linea = archivo.readline()

        while linea != "" and pacienteEncontrado is None:
            datos = linea.rstrip("\n").split(";")

            if len(datos) == 4 and datos[0] == dni:
                pacienteEncontrado = {
                    "dni": datos[0],
                    "nombre": datos[1],
                    "apellido": datos[2],
                    "cobertura": datos[3]
                }

            linea = archivo.readline()

    except FileNotFoundError:
        pass
    except OSError as mensaje:
        print("No se pudo leer el archivo de pacientes:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return pacienteEncontrado


def registrarPaciente():
    dni = pedirDni("Ingrese el DNI del paciente: ")

    if buscarPacientePorDNI(dni) is not None:
        print("Ya existe un paciente con ese DNI")
        return

    nombre = input("Ingrese el nombre del paciente: ").strip()

    while not validarTexto(nombre):
        print("El nombre no puede estar vacío ni contener punto y coma.")
        nombre = input("Ingrese nuevamente el nombre: ").strip()

    apellido = input("Ingrese el apellido del paciente: ").strip()

    while not validarTexto(apellido):
        print("El apellido no puede estar vacío ni contener punto y coma.")
        apellido = input("Ingrese nuevamente el apellido: ").strip()

    cobertura = input(
        "Ingrese la cobertura del paciente (deje en blanco para Particular): "
    ).strip()

    while cobertura != "" and not validarTexto(cobertura):
        print("La cobertura no puede contener punto y coma.")
        cobertura = input("Ingrese nuevamente la cobertura: ").strip()

    if cobertura == "":
        cobertura = "Particular"

    archivo = None

    try:
        archivo = open(ARCHIVO_PACIENTES, "at", encoding="utf-8")
        archivo.write(
            dni + ";" + nombre + ";" + apellido + ";" + cobertura + "\n"
        )
        print("Paciente registrado correctamente")

    except OSError as mensaje:
        print("No se pudo guardar el paciente:", mensaje)

    finally:
        if archivo is not None:
            archivo.close()


def listarPacientes():
    archivo = None
    hayPacientes = False

    try:
        archivo = open(ARCHIVO_PACIENTES, "rt", encoding="utf-8")
        linea = archivo.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")

            if len(datos) == 4:
                hayPacientes = True
                print("DNI: " + datos[0])
                print("Nombre: " + datos[1])
                print("Apellido: " + datos[2])
                print("Cobertura: " + datos[3])
                print()

            linea = archivo.readline()

        if not hayPacientes:
            print("No hay pacientes registrados")

    except FileNotFoundError:
        print("No hay pacientes registrados")
    except OSError as mensaje:
        print("No se pudo leer el archivo de pacientes:", mensaje)

    finally:
        if archivo is not None:
            archivo.close()


def mostrarPacientePorDNI():
    dni = pedirDni("Ingrese el DNI del paciente que desea buscar: ")
    paciente = buscarPacientePorDNI(dni)

    if paciente is None:
        print("No se encontró ningún paciente con ese DNI")
    else:
        print("Paciente encontrado:")
        print("DNI: " + paciente["dni"])
        print("Nombre: " + paciente["nombre"])
        print("Apellido: " + paciente["apellido"])
        print("Cobertura: " + paciente["cobertura"])


def _reescribirPaciente(dni, pacienteNuevo=None):
    archivoOriginal = None
    archivoAuxiliar = None
    encontrado = False
    operacionCorrecta = False

    try:
        archivoOriginal = open(ARCHIVO_PACIENTES, "rt", encoding="utf-8")
        archivoAuxiliar = open(ARCHIVO_AUXILIAR, "wt", encoding="utf-8")
        linea = archivoOriginal.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")

            if len(datos) == 4 and datos[0] == dni and not encontrado:
                encontrado = True

                if pacienteNuevo is not None:
                    archivoAuxiliar.write(
                        pacienteNuevo["dni"] + ";" +
                        pacienteNuevo["nombre"] + ";" +
                        pacienteNuevo["apellido"] + ";" +
                        pacienteNuevo["cobertura"] + "\n"
                    )
            else:
                archivoAuxiliar.write(linea)

            linea = archivoOriginal.readline()

        archivoOriginal.close()
        archivoOriginal = None

        archivoAuxiliar.close()
        archivoAuxiliar = None

        if encontrado:
            os.remove(ARCHIVO_PACIENTES)
            os.rename(ARCHIVO_AUXILIAR, ARCHIVO_PACIENTES)
            operacionCorrecta = True
        else:
            os.remove(ARCHIVO_AUXILIAR)
            print("No se encontró ningún paciente con ese DNI.")

    except FileNotFoundError:
        print("No hay pacientes registrados.")

    except OSError as mensaje:
        print("No se pudo actualizar el archivo de pacientes:", mensaje)

    finally:
        if archivoOriginal is not None:
            archivoOriginal.close()

        if archivoAuxiliar is not None:
            archivoAuxiliar.close()

    return operacionCorrecta


def eliminarPaciente():
    dni = pedirDni("Ingrese el DNI del paciente que desea eliminar: ")

    if buscarPacientePorDNI(dni) is None:
        print("No se encontró ningún paciente con ese DNI")
    elif _reescribirPaciente(dni):
        print("Paciente eliminado correctamente")


def modificarPaciente():
    dni = pedirDni("Ingrese el DNI del paciente que desea modificar: ")
    paciente = buscarPacientePorDNI(dni)

    if paciente is None:
        print("No se encontró ningún paciente con ese DNI")
        return

    nombre = input(
        "Ingrese el nuevo nombre del paciente (deje vacío para no modificar): "
    ).strip()

    while nombre != "" and not validarTexto(nombre):
        print("El nombre no puede contener punto y coma.")
        nombre = input("Ingrese nuevamente el nombre: ").strip()

    apellido = input(
        "Ingrese el nuevo apellido del paciente (deje vacío para no modificar): "
    ).strip()

    while apellido != "" and not validarTexto(apellido):
        print("El apellido no puede contener punto y coma.")
        apellido = input("Ingrese nuevamente el apellido: ").strip()

    cobertura = input(
        "Ingrese la nueva cobertura del paciente (deje vacío para no modificar): "
    ).strip()

    while cobertura != "" and not validarTexto(cobertura):
        print("La cobertura no puede contener punto y coma.")
        cobertura = input("Ingrese nuevamente la cobertura: ").strip()

    if nombre:
        paciente["nombre"] = nombre

    if apellido:
        paciente["apellido"] = apellido

    if cobertura:
        paciente["cobertura"] = cobertura

    if _reescribirPaciente(dni, paciente):
        print("Paciente modificado correctamente")


def menu():
    eleccion = 0

    while eleccion != 6:
        eleccion = input(
            "Gestión de pacientes, ingrese: \n"
            "1 para registrar un paciente. \n"
            "2 para listar los pacientes. \n"
            "3 para buscar un paciente por DNI. \n"
            "4 para modificar un paciente. \n"
            "5 para eliminar un paciente. \n"
            "6 para volver al menú principal. \n"
        )

        while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > 6:
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 6: ")

        eleccion = int(eleccion)

        match eleccion:
            case 1:
                registrarPaciente()

            case 2:
                listarPacientes()

            case 3:
                mostrarPacientePorDNI()

            case 4:
                modificarPaciente()

            case 5:
                eliminarPaciente()

            case 6:
                print("Volviendo al menú principal")

