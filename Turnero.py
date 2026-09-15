import Profesionales


turnos = []


def validarHora(hora):
    partes = hora.split(":")
    horaValida = False

    if len(partes) == 2:
        if len(partes[0]) == 2 and len(partes[1]) == 2:
            if partes[0].isdigit() and partes[1].isdigit():
                horas = int(partes[0])
                minutos = int(partes[1])

                if 0 <= horas <= 23 and 0 <= minutos <= 59:
                    horaValida = True

    return horaValida


def obtenercantdias(mes, año):
    if mes in [1, 3, 5, 7, 8, 10, 12]:
        dias = 31
    elif mes in [4, 6, 9, 11]:
        dias = 30
    elif mes == 2:
        if (año % 4 == 0 and año % 100 != 0) or año % 400 == 0:
            dias = 29
        else:
            dias = 28
    else:
        dias = -1

    return dias


def validarFecha(fecha):
    partes = fecha.split("/")
    fechaValida = False

    if len(partes) == 3:
        if (
            partes[0].isdigit()
            and partes[1].isdigit()
            and partes[2].isdigit()
        ):
            dia = int(partes[0])
            mes = int(partes[1])
            año = int(partes[2])

            cantidadDias = obtenercantdias(mes, año)

            if 1 <= dia <= cantidadDias:
                fechaValida = True

    return fechaValida


def darTurno():
    print("Seleccione un profesional...")
    Profesionales.mostrarProfesionales()

    matricula = input("Ingrese Matricula del profesional: ")

    profesionalesEncontrados = False

    for profesional in Profesionales.profesionales:
        if profesional[0] == matricula:
            profesionalesEncontrados = True

    if profesionalesEncontrados:
        dni = input("Ingrese DNI del paciente")

        while not (len(dni) == 7 or len(dni) == 8) or not dni.isdigit():
            print("DNI no válido")
            dni = input("Ingrese nuevamente el DNI del paciente")

        fecha = input("Ingrese la fecha con formato día/mes/año: ")

        while not validarFecha(fecha):
            print("Fecha incorrecta")
            fecha = input("Ingrese de nuevo la fecha: ")

        hora = input("Ingrese la hora: ")

        while not validarHora(hora):
            print("Hora incorrecta")
            hora = input("Ingrese nuevamente la hora: ")

        horarioOcupado = False

        for turno in turnos:
            if (
                turno[1] == matricula
                and turno[2] == fecha
                and turno[3] == hora
            ):
                horarioOcupado = True

        if horarioOcupado:
            print("El profesional ya tiene un turno en esa fecha y hora")

        else:
            turnos.append([
                dni,
                matricula,
                fecha,
                hora
            ])

            print("Turno dado correctamente")

    else:
        print("No se ha encontrado a ningún profesional con el ID ingresado")


def reprogramarTurno():
    dni = input("Ingrese DNI del paciente")

    while not (len(dni) == 7 or len(dni) == 8) or not dni.isdigit():
        print("DNI no valido")
        dni = input("Ingrese nuevamente el DNI del paciente")

    turnosPaciente = []

    for turno in turnos:
        if turno[0] == dni:
            turnosPaciente.append(turno)

    if len(turnosPaciente) == 0:
        print("No hay turnos para el DNI del paciente")

    else:
        print("Estos son los turnos del paciente")

        for i in range(len(turnosPaciente)):
            print("Turno", i + 1)
            print("Profesional ID: " + turnosPaciente[i][1])
            print("Fecha: " + turnosPaciente[i][2])
            print("Hora: " + turnosPaciente[i][3])
            print()

        opcionesValidas = []

        for i in range(1, len(turnosPaciente) + 1):
            opcionesValidas.append(str(i))

        opcion = input(
            "Ingrese el número del turno que desea modificar: "
        )

        while opcion not in opcionesValidas:
            print("Opción incorrecta")
            opcion = input("Seleccione nuevamente el turno: ")

        opcion = int(opcion)

        turnoReprogramar = turnosPaciente[opcion - 1]

        fecha = input("Ingrese la nueva fecha: ")

        while not validarFecha(fecha):
            print("Fecha incorrecta")
            fecha = input("Ingrese de nuevo la fecha: ")

        hora = input("Ingrese la nueva hora: ")

        while not validarHora(hora):
            print("Hora incorrecta")
            hora = input("Ingrese nuevamente la hora: ")

        horarioOcupado = False

        for turno in turnos:
            if (
                turno != turnoReprogramar
                and turno[1] == turnoReprogramar[1]
                and turno[2] == fecha
                and turno[3] == hora
            ):
                horarioOcupado = True

        if horarioOcupado:
            print(
                "No es posible reprogramar la cita debido a que "
                "el profesional ya tiene un turno esa fecha y hora"
            )

        else:
            turnoReprogramar[2] = fecha
            turnoReprogramar[3] = hora

            print("Turno reprogramado correctamente")


def cancelarTurno():
    dni = input("Ingrese DNI del paciente")

    while not (len(dni) == 7 or len(dni) == 8) or not dni.isdigit():
        print("DNI no valido")
        dni = input("Ingrese nuevamente el DNI del paciente")

    turnoEncontrado = False
    turnoCancelar = []

    for turno in turnos:
        if turno[0] == dni and not turnoEncontrado:
            turnoCancelar = turno
            turnoEncontrado = True

    if turnoEncontrado:
        turnos.remove(turnoCancelar)
        print("Turno cancelado")

    else:
        print("No se encontró un turno para el paciente ingresado")


def listarTurnos():
    dni = input("Ingrese DNI del paciente")

    while not (len(dni) == 7 or len(dni) == 8) or not dni.isdigit():
        print("DNI no válido")
        dni = input("Ingrese nuevamente el DNI del paciente")

    turnoEncontrado = False

    for turno in turnos:
        if turno[0] == dni:
            print("Paciente DNI: " + turno[0])
            print("Profesional ID: " + turno[1])
            print("Fecha: " + turno[2])
            print("Hora: " + turno[3])
            print()

            turnoEncontrado = True

    if not turnoEncontrado:
        print("No se han encontrado turnos para el DNI ingresado")