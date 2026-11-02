
def validarDni(dni):
    return (len(dni) == 7 or len(dni) == 8) and dni.isdigit()


def buscarPacientePorDNI(pacientes, dni):
    return pacientes.get(dni, None)


def registrarPaciente(pacientes):
    dni = input("Ingrese el DNI del paciente: ")

    while not validarDni(dni):
        print("DNI no válido")
        dni = input("Ingrese nuevamente el DNI del paciente: ")

    if buscarPacientePorDNI(pacientes, dni) is not None:
        print("Ya existe un paciente con ese DNI")
        return

    nombre = input("Ingrese el nombre del paciente: ")
    apellido = input("Ingrese el apellido del paciente: ")
    cobertura = input("Ingrese la cobertura del paciente (deje en blanco para Particular): ")
    pacientes[dni] = {
        "nombre": nombre,
        "apellido": apellido,
        "cobertura": cobertura if cobertura else "Particular"
    }

    print("Paciente registrado correctamente")



def listarPacientes(pacientes):
    if not pacientes:
        print("No hay pacientes registrados")
    else:
        print("Pacientes registrados:")

        for dni in pacientes:
            print("DNI: " + dni)
            print("Nombre: " + pacientes[dni]["nombre"])
            print("Apellido: " + pacientes[dni]["apellido"])
            print("Cobertura: " + pacientes[dni]["cobertura"])
            print()


def mostrarPacientePorDNI(pacientes):
    dni = input("Ingrese el DNI del paciente que desea buscar: ")

    paciente = buscarPacientePorDNI(pacientes, dni)

    if paciente is None:
        print("No se encontró ningún paciente con ese DNI")
    else:
        print("Paciente encontrado:")
        print("DNI: " + dni)
        print("Nombre: " + paciente["nombre"])
        print("Apellido: " + paciente["apellido"])
        print("Cobertura: " + paciente["cobertura"])

def eliminarPaciente(pacientes):
    dni = input("Ingrese el DNI del paciente que desea eliminar: ")

    paciente = buscarPacientePorDNI(pacientes, dni)

    if paciente is None:
        print("No se encontró ningún paciente con ese DNI")
    else:
        del pacientes[dni]
        print("Paciente eliminado correctamente")

def modificarPaciente(pacientes):
    dni = input("Ingrese el DNI del paciente que desea modificar: ")

    paciente = buscarPacientePorDNI(pacientes, dni)

    if paciente is None:
        print("No se encontró ningún paciente con ese DNI")
    else:
        nombre = input("Ingrese el nuevo nombre del paciente (deje vacío para no modificar): ")
        apellido = input("Ingrese el nuevo apellido del paciente (deje vacío para no modificar): ")
        cobertura = input("Ingrese la nueva cobertura del paciente (deje vacío para no modificar): ")
        if nombre:
            paciente["nombre"] = nombre
        if apellido:
            paciente["apellido"] = apellido
        if cobertura:
            paciente["cobertura"] = cobertura

        print("Paciente modificado correctamente")

def menu(pacientes):
    eleccion = 0

    while eleccion != 4:
        eleccion = input(
            "Gestión de pacientes, ingrese: \n"
            "1 para registrar un paciente. \n"
            "2 para listar los pacientes. \n"
            "3 para buscar un paciente por DNI. \n"
            "4 para modificar un paciente. \n"
            "5 para eliminar un paciente. \n"
            "6 para volver al menú principal. \n"
        )

        while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > 4:
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 4: ")

        eleccion = int(eleccion)

        match eleccion:
            case 1:
                registrarPaciente(pacientes)
            case 2:
                listarPacientes(pacientes)
            case 3:
                mostrarPacientePorDNI(pacientes)
            case 4:
                modificarPaciente(pacientes)
            case 5:
                eliminarPaciente(pacientes)
            case 6:
                print("Volviendo al menú principal")
