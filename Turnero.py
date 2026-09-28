from datetime import datetime
import Profesionales
import Pacientes

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

def validarFechaHoraFutura(fecha, hora):
    partesFecha = fecha.split("/")
    partesHora = hora.split(":")

    dia = int(partesFecha[0])
    mes = int(partesFecha[1])
    año = int(partesFecha[2])
    horas = int(partesHora[0])
    minutos = int(partesHora[1])

    fechaHoraTurno = datetime(año,mes,dia,horas, minutos)
    fechaHoraActual = datetime.now()

    fechaHoraValida = False

    if fechaHoraTurno > fechaHoraActual:
        fechaHoraValida = True
    return fechaHoraValida

def ingresarFechaHora():
    fechaHoraValida = False
    fecha = ""
    hora = ""

    while not fechaHoraValida:
        fecha = input("Ingrese la fecha con formato día/mes/año: \n")

        while not validarFecha(fecha):
            print("Fecha incorrecta")
            fecha = input("Ingrese de nuevo la fecha: \n")

        hora = input("Ingrese la hora con formato HH:MM: \n")

        while not validarHora(hora):
            print("Hora incorrecta")
            hora = input("Ingrese nuevamente la hora: \n")

        if validarFechaHoraFutura(fecha, hora):
            fechaHoraValida = True
        else:
            print("No se puede asignar un turno en una fecha u hora pasada")

    return fecha, hora

def darTurno(profesionales, pacientes, turnos):
    print("Seleccione un profesional...")
    Profesionales.mostrarProfesionales(profesionales)

    legajo = input("Ingrese legajo del profesional: \n")

    profesionalesEncontrados = False

    for profesional in profesionales:
        if profesional[0] == legajo:
            profesionalesEncontrados = True

    if profesionalesEncontrados:
        legajoPaciente = input("Ingrese el legajo del paciente: ")

        pacienteEncontrado = Pacientes.buscarPacientePorLegajo(pacientes, legajoPaciente)

        while pacienteEncontrado is None:
            print("No existe un paciente registrado con ese legajo")
            legajoPaciente = input("Ingrese nuevamente el legajo del paciente: ")

            pacienteEncontrado = Pacientes.buscarPacientePorLegajo(pacientes, legajoPaciente)
        fecha, hora = ingresarFechaHora()

        horarioOcupado = False

        for turno in turnos:
            if (
                turno[1] == legajo
                and turno[2] == fecha
                and turno[3] == hora
            ):
                horarioOcupado = True

        if horarioOcupado:
            print("El profesional ya tiene un turno en esa fecha y hora, los horarios que tiene ocupados son: \n")
            for turno in turnos:
                if (
                    turno[1] == legajo
                    and turno[2] == fecha
                ):
                    print(" - " + turno[3])
            print("El rango horario del profesional es de: " + Profesionales.getHorarioProfesional(profesionales, legajo) + ", ingrese un nuevo horario dentro del rango. \n")
        else:
            turnos.append([
                legajoPaciente,
                legajo,
                fecha,
                hora
            ])

            print("Turno dado correctamente \n")

    else:
        print("No se ha encontrado a ningún profesional con el legajo ingresado \n")


def reprogramarTurno(turnos):
    if not turnos: #si no hay turnos no tiene sentido seguir con la funcion, esto se replica en todos los casos que sea necesario
        print("No hay turnos registrados en el sistema. \n")
        return
    
    legajoPaciente = input("Ingrese el legajo del paciente: ")

    turnosPaciente = []

    for turno in turnos:
        if turno[0] == legajoPaciente:
            turnosPaciente.append(turno)

    if not turnosPaciente:
        print("No hay turnos asignados para el legajo: " + legajoPaciente + "\n")

    else:
        print("Estos son los turnos del paciente \n")

        for i in range(len(turnosPaciente)):
            print("Turno", i + 1)
            print("Legajo del profesional: " + turnosPaciente[i][1])
            print("Fecha: " + turnosPaciente[i][2])
            print("Hora: " + turnosPaciente[i][3])
            print()

        opcionesValidas = []

        for i in range(1, len(turnosPaciente) + 1):
            opcionesValidas.append(str(i))

        opcion = input(
            "Ingrese el número del turno que desea modificar: \n"
        )

        while opcion not in opcionesValidas:
            print("Opción incorrecta")
            opcion = input("Seleccione nuevamente el turno: \n ")

        opcion = int(opcion)

        turnoReprogramar = turnosPaciente[opcion - 1]

        fecha, hora = ingresarFechaHora()
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
                "el profesional ya tiene un turno esa fecha y hora, elija otro horario \n"
            )

        else:
            turnoReprogramar[2] = fecha
            turnoReprogramar[3] = hora

            print("Turno reprogramado correctamente \n")


def cancelarTurno(turnos):
    if not turnos:
        print("No hay turnos registrados en el sistema. \n")
        return
    
    legajoPaciente = input("Ingrese el legajo del paciente: ")
    
    turnosPaciente = []


    for turno in turnos:
        if turno[0] == legajoPaciente:
            turnosPaciente.append(turno)

    if not turnosPaciente:
        print("No hay turnos registrados en el sistema para el legajo. \n" + legajoPaciente)
    else:
        print("Estos son los turnos del paciente \n")

        for posicion in range(len(turnosPaciente)):
            print("Turno", posicion + 1)
            print("Legajo del profesional: " + turnosPaciente[posicion][1])
            print("Fecha: " + turnosPaciente[posicion][2])
            print("Hora: " + turnosPaciente[posicion][3])
            print()

        opcionesValidas = []

        for posicion in range(1, len(turnosPaciente) + 1):
            opcionesValidas.append(str(posicion))

        opcion = input("Ingrese el número del turno que desea cancelar: ")

        while opcion not in opcionesValidas:
            print("Opcion incorrecta")
            opcion = input("Seleccione nuevamente el turno: \n ")

        opcion = int(opcion)

        turnoCancelar = turnosPaciente[opcion - 1]
        turnos.remove(turnoCancelar)

        print("Turno cancelado correctamente")

def listarTodosLosTurnos(turnos):
    if not turnos:
        print("No hay turnos registrados en el sistema. \n")
    else:
        print("Estos son todos los turnos en el sistema \n")

        for turno in turnos:
            print("Legajo del paciente: " + turno[0])
            print("Legajo del profesional: " + turno[1])
            print("Fecha: " + turno[2])
            print("Hora: " + turno[3])
            print()