from datetime import datetime

import Especialidades
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
#Comprueba que la fecha y la hora elegidas sean posteriores al momento actual para evitar asignar turnos pasados.
def validarFechaHoraFutura(fecha, hora):
    partesFecha = fecha.split("/")
    partesHora = hora.split(":")

    dia = int(partesFecha[0])
    mes = int(partesFecha[1])
    año = int(partesFecha[2])
    horas = int(partesHora[0])
    minutos = int(partesHora[1])

    #Construimos la fecha del turno y obtenemos la fecha actual para poder compararlas.
    fechaHoraTurno = datetime(año,mes,dia,horas, minutos)
    fechaHoraActual = datetime.now()

    fechaHoraValida = False

    #La fecha solamente es válida si ocurre después del momento actual.
    if fechaHoraTurno > fechaHoraActual:
        fechaHoraValida = True
    return fechaHoraValida

#Solicita una fecha y una hora hasta que tengan un formato correcto y correspondan a un momento futuro
def ingresarFechaHora():
    fechaHoraValida = False
    fecha = ""
    hora = ""

    #El bucle termian cuando tanto el formato como el momento de la cita son válidos
    while not fechaHoraValida:
        fecha = input("Ingrese la fecha con formato día/mes/año: \n")

    #Se vuelve a solicitar la fecha mientras su formato o sus valores no sean correctos
        while not validarFecha(fecha):
            print("Fecha incorrecta")
            fecha = input("Ingrese de nuevo la fecha: \n")

        hora = input("Ingrese la hora con formato HH:MM: \n")
    #Se vuelve a solicitar la hora mientras no tenga un formato HH:MM válido
        while not validarHora(hora):
            print("Hora incorrecta")
            hora = input("Ingrese nuevamente la hora: \n")
    #Aunque el formato sea correcto, no se admiten fechas u horas que ya hayan pasado.
        if validarFechaHoraFutura(fecha, hora):
            fechaHoraValida = True
        else:
            print("No se puede asignar un turno en una fecha u hora pasada")

    return fecha, hora

#Obtiene el nombre del día de la semana correspondiente a una fecha introducida con formato día/mes/año
def obtenerDiaSemana(fecha):
    partesFecha = fecha.split("/")
    dia = int(partesFecha[0])
    mes = int(partesFecha[1])
    año = int(partesFecha[2])

    fechaTurno = datetime(año,mes, dia)

    #La función weekday devuelve un número del 0 al 6, donde 0 es lunes y 6 domingo.
    diasSemana = ["lunes","martes","miércoles","jueves", "viernes", "sábado", "domingo"]
    diaSemana = diasSemana[fechaTurno.weekday()]
    return diaSemana


#Comprueba que el profesional atiende el día del turno y que la hora elegida esté dentro de su jornada
def validarHorarioProfesional(profesionales, legajo, fecha, hora):
    horarioValido = False

    #Obtenemos el día para consultar su horario en el diccionario
    diaSemana = obtenerDiaSemana(fecha)

    for profesional in profesionales:
        if profesional[0] == legajo:
            #La posición 3 contiene los horarios del profesional
            horarios = profesional[3]
            horarioDia = horarios[diaSemana]

            if horarioDia:
                partesHora = hora.split(":")
                partesInicio = horarioDia[0].split(":")
                partesFinal = horarioDia[1].split(":")

                minutosHora = (int(partesHora[0]) * 60 + int(partesHora[1]))
                minutosInicio =(int(partesInicio[0]) * 60 + int(partesInicio[1]))
                minutosFin = (int(partesFinal[0]) * 60 + int(partesFinal[1]))

                if(minutosInicio <= minutosHora and minutosHora < minutosFin):
                    horarioValido = True
    return horarioValido


def darTurno(profesionales, pacientes, turnos, especialidades):

    if not especialidades:
        print("No hay especialidades registradas")
        return

    # Seleccionamos la especialidad mediante su número
    Especialidades.listarEspecialidades(especialidades)

    opcion = input("Seleccione el número de la especialidad: ")

    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(especialidades):
        print("Opción incorrecta")
        opcion = input("Seleccione nuevamente la especialidad: ")

    especialidad = especialidades[int(opcion) - 1]

    profesionalesEspecialidad = Profesionales.buscarProfesionalesPorEspecialidad(
        profesionales, especialidad
    )

    if not profesionalesEspecialidad:
        print("No hay profesionales registrados para esa especialidad")
        return

    # Comprobamos que el paciente esté registrado
    dni = input("Ingrese el DNI del paciente: ")

    pacienteEncontrado = Pacientes.buscarPacientePorDNI(pacientes, dni)

    while pacienteEncontrado is None:

        print("No existe un paciente registrado con ese DNI, ¿querés registrarlo? (S/N)")
        opcion = input("Ingrese su elección: ")

        if opcion.upper() == "S":
            Pacientes.registrarPaciente(pacientes)

        dni = input("Ingrese nuevamente el DNI del paciente: ")

        pacienteEncontrado = Pacientes.buscarPacientePorDNI(pacientes, dni)

    # Buscamos el primer turno disponible desde la fecha actual
    resultado = Profesionales.buscarPrimerTurnoLibre(
        profesionalesEspecialidad, turnos, especialidad, dni
    )

    profesionalEncontrado = None
    fecha = ""
    hora = ""
    esSobreturno = False

    if resultado is not None:

        profesionalEncontrado, fecha, hora, esSobreturno = resultado

        print("\nPrimer turno disponible:")
        print("Profesional:", profesionalEncontrado[1])
        print("Fecha:", fecha)
        print("Hora:", hora)

        if esSobreturno:
            print("Tipo: Sobreturno")

        opcion = input("¿Desea aceptar este turno? (S/N): ")

    else:
        print("No se encontraron turnos disponibles automáticamente")
        opcion = "N"

    # Si el paciente no acepta, puede buscar manualmente
    if opcion.upper() != "S":

        turnoValido = False

        while not turnoValido:

            fecha, hora = ingresarFechaHora()

            diaSemana = obtenerDiaSemana(fecha)

            profesionalEncontrado = Profesionales.buscarProfesionalParaFechaHora(
                profesionalesEspecialidad,
                turnos,
                especialidad,
                dni,
                diaSemana,
                fecha,
                hora
            )

            if profesionalEncontrado is None:
                print("No hay profesionales disponibles para esa fecha y hora")
            else:
                turnoValido = True

                # Comprobamos si el horario corresponde a un sobreturno
                partesHora = hora.split(":")
                minutosHora = int(partesHora[0]) * 60 + int(partesHora[1])

                partesFin = profesionalEncontrado[3][diaSemana][1].split(":")
                minutosFin = int(partesFin[0]) * 60 + int(partesFin[1])

                esSobreturno = minutosHora >= minutosFin

    # Registramos el turno
    legajo = profesionalEncontrado[0]

    turnos.append([dni, legajo, fecha, hora])

    print("\nTurno dado correctamente")
    print("Paciente:", pacienteEncontrado["nombre"], pacienteEncontrado["apellido"])
    print("Profesional:", profesionalEncontrado[1])
    print("Especialidad:", profesionalEncontrado[2])
    print("Fecha:", fecha)
    print("Hora:", hora)

    if esSobreturno:
        print("Turno asignado como sobreturno")


#Permite seleccionar uno de los turnos del paciente y cambiar su fecha y hora respetando el horario del profesional.
# Permite reprogramar un turno, mantener la especialidad o elegir otra.
def reprogramarTurno(profesionales, turnos, especialidades):
    if not turnos:
        print("No hay turnos registrados en el sistema. \n")
        return

    dniPaciente = input("Ingrese el DNI del paciente: ")

    turnosPaciente = []

    for turno in turnos:
        if turno[0] == dniPaciente:
            turnosPaciente.append(turno)

    if not turnosPaciente:
        print("No hay turnos asignados para el DNI: " + dniPaciente + "\n")
        return

    print("Estos son los turnos del paciente:\n")

    for posicion in range(len(turnosPaciente)):
        print("Turno", posicion + 1)
        print("Legajo del profesional: " + turnosPaciente[posicion][1])
        print("Fecha: " + turnosPaciente[posicion][2])
        print("Hora: " + turnosPaciente[posicion][3])
        print()

    opcionesValidas = []

    for posicion in range(1, len(turnosPaciente) + 1):
        opcionesValidas.append(str(posicion))

    opcion = input("Ingrese el número del turno que desea reprogramar: ")

    while opcion not in opcionesValidas:
        print("Opción incorrecta")
        opcion = input("Seleccione nuevamente el turno: ")

    turnoReprogramar = turnosPaciente[int(opcion) - 1]

    # Averiguamos la especialidad que tenía el turno original.
    especialidadActual = ""

    for profesional in profesionales:
        if profesional[0] == turnoReprogramar[1]:
            especialidadActual = profesional[2]
            break

    if especialidadActual == "":
        print("No se encontró el profesional del turno seleccionado")
        return

    print("\nSeleccione cómo desea buscar el nuevo turno:")
    print("1. Buscar el primer turno disponible de la misma especialidad (" + especialidadActual + ")")
    print("2. Elegir manualmente fecha y hora de la misma especialidad")
    print("3. Cambiar de especialidad y buscar disponibilidad")
    print("4. Volver")

    opcion = input("Ingrese una opción: ")

    while opcion not in ["1", "2", "3", "4"]:
        print("Opción incorrecta")
        opcion = input("Ingrese una opción entre 1 y 4: ")

    if opcion == "4":
        return

    especialidadElegida = especialidadActual

    if opcion == "3":
        if not especialidades:
            print("No hay especialidades registradas")
            return

        Especialidades.listarEspecialidades(especialidades)
        seleccion = input("Seleccione el número de la nueva especialidad: ")

        while not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(especialidades):
            print("Opción incorrecta")
            seleccion = input("Seleccione nuevamente la especialidad: ")

        especialidadElegida = especialidades[int(seleccion) - 1]

    profesionalesEspecialidad = Profesionales.buscarProfesionalesPorEspecialidad(
        profesionales, especialidadElegida
    )

    if not profesionalesEspecialidad:
        print("No hay profesionales registrados para esa especialidad")
        return

    # En la búsqueda automática excluimos el turno original para que no se bloquee a sí mismo.
    if opcion == "1" or opcion == "3":
        resultado = Profesionales.buscarPrimerTurnoLibre(
            profesionalesEspecialidad, turnos, especialidadElegida,
            dniPaciente, turnoReprogramar
        )

        if resultado is not None:
            profesionalNuevo, fechaNueva, horaNueva, esSobreturno = resultado

            print("\nPrimer turno disponible:")
            print("Profesional:", profesionalNuevo[1])
            print("Especialidad:", profesionalNuevo[2])
            print("Fecha:", fechaNueva)
            print("Hora:", horaNueva)

            if esSobreturno:
                print("Tipo: Sobreturno")

            aceptar = input("¿Desea reprogramar el turno para esta fecha? (S/N): ")

            if aceptar.upper() == "S":
                turnoReprogramar[1] = profesionalNuevo[0]
                turnoReprogramar[2] = fechaNueva
                turnoReprogramar[3] = horaNueva
                print("Turno reprogramado correctamente")
                return
        else:
            print("No se encontraron turnos disponibles automáticamente")

        opcionManual = input("¿Desea elegir manualmente una fecha y hora? (S/N): ")
        if opcionManual.upper() != "S":
            print("El turno original se mantiene sin cambios")
            return

    # Búsqueda manual: puede asignarse cualquier profesional de la especialidad elegida.
    nuevoTurnoValido = False

    while not nuevoTurnoValido:
        fechaNueva, horaNueva = ingresarFechaHora()
        diaSemana = obtenerDiaSemana(fechaNueva)

        profesionalNuevo = Profesionales.buscarProfesionalParaFechaHora(
            profesionalesEspecialidad, turnos, especialidadElegida,
            dniPaciente, diaSemana, fechaNueva, horaNueva, turnoReprogramar
        )

        if profesionalNuevo is None:
            print("No hay profesionales disponibles para esa fecha y hora")
        else:
            nuevoTurnoValido = True

            turnoReprogramar[1] = profesionalNuevo[0]
            turnoReprogramar[2] = fechaNueva
            turnoReprogramar[3] = horaNueva

            print("\nTurno reprogramado correctamente")
            print("Profesional:", profesionalNuevo[1])
            print("Especialidad:", profesionalNuevo[2])
            print("Fecha:", fechaNueva)
            print("Hora:", horaNueva)

            partesHora = horaNueva.split(":")
            minutosHora = int(partesHora[0]) * 60 + int(partesHora[1])
            partesFin = profesionalNuevo[3][diaSemana][1].split(":")
            minutosFin = int(partesFin[0]) * 60 + int(partesFin[1])

            if minutosHora >= minutosFin:
                print("Turno asignado como sobreturno")


#Cancela uno de los turnos asignados al legajo de un paciente
def cancelarTurno(turnos):
    if not turnos:
        print("No hay turnos registrados en el sistema. \n")
        return
    
    dniPaciente = input("Ingrese el DNI del paciente: ")

    #Guardamos únicamente los turnos del paciente indicado
    turnosPaciente = []


    for turno in turnos:
        if turno[0] == dniPaciente:
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
            print("Opción incorrecta")
            opcion = input("Seleccione nuevamente el turno: \n ")

        opcion = int(opcion)

        #Eliminamos de la lista general el turno seleccionado
        turnoCancelar = turnosPaciente[opcion - 1]
        turnos.remove(turnoCancelar)

        print("Turno cancelado correctamente")

#Muestra todos los turnos registrados en el sistema
def listarTodosLosTurnos(turnos):
    if not turnos:
        print("No hay turnos registrados en el sistema. \n")
    else:
        print("Estos son todos los turnos en el sistema \n")

        for turno in turnos:
            print("DNI del paciente: " + turno[0])
            print("Legajo del profesional: " + turno[1])
            print("Fecha: " + turno[2])
            print("Hora: " + turno[3])
            print()