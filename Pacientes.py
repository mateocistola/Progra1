
#Comprobamos que el dni tenga siete u ocho dígitos
def validarDni(dni):
    dniValido = False

    if (len(dni) == 7 or len(dni) == 8) and dni.isdigit():
        dniValido = True

    return dniValido

#Buscamos un paciente utilizando su legajo como clave del diccionario
def buscarPacientePorLegajo(pacientes, legajo):
    pacienteEncontrado = pacientes.get(legajo)

    return pacienteEncontrado

#Comprobamos que el dni no pertenezca a otro paciente
def dniRegistrado(pacientes, dni):
    registrado = False

    for legajo in pacientes:
        if pacientes[legajo]["dni"] == dni:
            registrado = True

    return registrado

#Registramos un paciente si su legajo y su dni no están repetidos
def registrarPaciente(pacientes):
    legajo = input("Ingrese el legajo del paciente: ")

    pacienteEncontrado = buscarPacientePorLegajo(pacientes, legajo)

    if pacienteEncontrado is not None:
        print("ya existe un paciente con ese legajo")
    else:
        dni = input("Ingrese el DNI del paciente: ")

        while not validarDni(dni):
            print("DNI no válido")
            dni = input("Ingrese nuevamente el DNI del paciente: ")

        while dniRegistrado(pacientes, dni):
            print("Ya existe un paciente con ese DNI")
            dni = input("Ingrese otro DNI: ")

            while not validarDni(dni):
                print("DNI no válido")
                dni = input("Ingrese nuevamente el DNI: ")

        nombre = input("Ingrese el nombre del paciente: ")
        apellido = input("Ingrese el apellido del paciente: ")

        pacientes[legajo] = {"dni": dni, "nombre": nombre, "apellido": apellido}

        print("Paciente registrado correctamente")

#Mostramos todos los pacientes registrados
def listarPacientes(pacientes):
    if not pacientes:
        print("No hay pacientes registrados")
    else:
        print("Pacientes registrados:")

        for legajo in pacientes:
            print("Legajo: " + legajo)
            print("DNI: " + pacientes[legajo]["dni"])
            print("Nombre: " + pacientes[legajo]["nombre"])
            print("Apellido: " + pacientes[legajo]["apellido"])
            print()


#Busca y muestra los datos de un paciente por su legajo
def mostrarPacientePorLegajo(pacientes):
    legajo = input("Ingrese el legajo del paciente: ")

    pacienteEncontrado = buscarPacientePorLegajo(pacientes, legajo)

    if pacienteEncontrado is None:
        print("No hay pacientes registrados con ese legajo")
    else:
        print("Legajo: " + legajo)
        print("DNI: " + pacienteEncontrado["dni"])
        print("Nombre: " + pacienteEncontrado["nombre"])
        print("Apellido: " + pacienteEncontrado["apellido"])

#Mostramos las opciones disponibles para gestionar pacientes
def menu(pacientes):
    eleccion = 0

    while eleccion != 4:
        eleccion = input(
            "Gestión de pacientes, ingrese: \n"
            "1 para registrar un paciente. \n"
            "2 para listar los pacientes. \n"
            "3 para buscar un paciente por legajo. \n"
            "4 para volver al menú principal. \n"
        )

        while not eleccion.isdigit():
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 4: ")

        eleccion = int(eleccion)

        match eleccion:
            case 1:
                registrarPaciente(pacientes)
            case 2:
                listarPacientes(pacientes)
            case 3:
                mostrarPacientePorLegajo(pacientes)
            case 4:
                print("Volviendo al menú principal")
            case _:
                print("Opción incorrecta")