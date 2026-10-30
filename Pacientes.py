
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

    pacientes[dni] = {
        "dni": dni,
        "nombre": nombre,
        "apellido": apellido
    }

    print("Paciente registrado correctamente")



def listarPacientes(pacientes):
    if not pacientes:
        print("No hay pacientes registrados")
    else:
        print("Pacientes registrados:")

        for dni in pacientes:
            print("DNI: " + pacientes[dni]["dni"])
            print("Nombre: " + pacientes[dni]["nombre"])
            print("Apellido: " + pacientes[dni]["apellido"])
            print()


def mostrarPacientePorDNI(pacientes):
    dni = input("Ingrese el DNI del paciente que desea buscar: ")

    paciente = buscarPacientePorDNI(pacientes, dni)

    if paciente is None:
        print("No se encontró ningún paciente con ese DNI")
    else:
        print("Paciente encontrado:")
        print("DNI: " + paciente["dni"])
        print("Nombre: " + paciente["nombre"])
        print("Apellido: " + paciente["apellido"])


def menu(pacientes):
    eleccion = 0

    while eleccion != 4:
        eleccion = input(
            "Gestión de pacientes, ingrese: \n"
            "1 para registrar un paciente. \n"
            "2 para listar los pacientes. \n"
            "3 para buscar un paciente por DNI. \n"
            "4 para volver al menú principal. \n"
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
                print("Volviendo al menú principal")
