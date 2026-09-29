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

#Asigna un turno a un paciente registrado comprobando la existencia del profesional, su horario y la disponibilidad
def darTurno(profesionales, pacientes, turnos):
    print("Seleccione un profesional...")
    Profesionales.mostrarProfesionales(profesionales)

    legajo = input("Ingrese legajo del profesional: \n")

    #Buscamos al profesional por legajo utilizando la función recursiva del módulo Profesionales
    profesionalEncontrado = Profesionales.buscarProfesionalPorLegajo(profesionales, legajo)

    if profesionalEncontrado is not None:
        legajoPaciente = input("Ingrese el legajo del paciente: ")

        #El turno solo puede asignarse a un paciente previamente registrado en el sistema
        pacienteEncontrado = Pacientes.buscarPacientePorLegajo(pacientes, legajoPaciente)

        #Se vuelve a solicitar el legajo hasta encontrar un paciente registrado
        while pacienteEncontrado is None:
            print("No existe un paciente registrado con ese legajo")
            legajoPaciente = input("Ingrese nuevamente el legajo del paciente: ")

            pacienteEncontrado = Pacientes.buscarPacientePorLegajo(pacientes, legajoPaciente)

        #El turno solamente se guardará cuando cumpla todas las condiciones necesarias
        turnoValido = False

        #Si existe algún problema, se solicita otra fecha y hora
        while not turnoValido:
            fecha, hora = ingresarFechaHora()

        #Comprobamos que el profesional atienda ese día y que la hora esté dentro de su jornada
            horarioValido = validarHorarioProfesional(profesionales, legajo, fecha, hora)

        #Si el horario no es válido, mostramos el horario del profesional para el día seleccionado
            if not horarioValido:
                diaSemana = obtenerDiaSemana(fecha)

                print("El profesional no atiende ese día o esa hora")
                print("Horario del " + diaSemana + ": " + Profesionales.getHorarioProfesional(profesionales, legajo, diaSemana))
            else:

                #Nos permite comprobar por separado la disponibilidad del profesional y del paciente
                horarioOcupado = False
                pacienteOcupado = False

                for turno in turnos:

                    #El profesional no puede tener dos turnos en la misma fecha y hora
                    if (
                        turno[1] == legajo
                        and turno[2] == fecha
                        and turno[3] == hora
                    ):
                        horarioOcupado = True
                    if (
                        #El paciente tampoco puede tener dos turnos en la misma fecha y hora
                        turno[0] == legajoPaciente
                        and turno[2] == fecha
                        and turno[3] == hora
                    ):
                        pacienteOcupado = True
                if horarioOcupado:
                    print("El profesional ya tiene un turno en esa fecha y hora, los horarios que tiene ocupados son: \n")
                    for turno in turnos:
                        if (
                            turno[1] == legajo
                            and turno[2] == fecha
                        ):
                            print(" - " + turno[3])
                elif pacienteOcupado:
                    print("El paciente ya tiene otro turno en esa fecha y hora")
                else:
                    #Todas las comprobaciones fueron correctas, por lo que podemos finalizar el bucle
                    turnoValido = True

        #Guardamos los legajos, la fecha y la hora del turno
        turnos.append([legajoPaciente, legajo, fecha, hora])

        print("Turno dado correctamente \n")

    else:
        print("No se ha encontrado a ningún profesional con el legajo ingresado \n")


#Permite seleccionar uno de los turnos del paciente y cambiar su fecha y hora respetando el horario del profesional.
def reprogramarTurno(profesionales, turnos):
    if not turnos: #si no hay turnos no tiene sentido seguir con la función, esto se replica en todos los casos que sea necesario
        print("No hay turnos registrados en el sistema. \n")
        return
    
    legajoPaciente = input("Ingrese el legajo del paciente: ")

    #Guardamos en una lista solamente los turnos que pertenecen al paciente indicado
    turnosPaciente = []

    for turno in turnos:
        #La posición 0 contiene el legajo del paciente
        if turno[0] == legajoPaciente:
            turnosPaciente.append(turno)

    if not turnosPaciente:
        print("No hay turnos asignados para el legajo: " + legajoPaciente + "\n")

    else:
        print("Estos son los turnos del paciente \n")

        #Mostramos los turnos con una numeración que empieza en el 1
        for posicion in range(len(turnosPaciente)):
            print("Turno", posicion + 1)
            print("Legajo del profesional: " + turnosPaciente[posicion][1])
            print("Fecha: " + turnosPaciente[posicion][2])
            print("Hora: " + turnosPaciente[posicion][3])
            print()

        #Creamos las opciones válidas según la cantidad de turnos que tenga el paciente.
        opcionesValidas = []

        for posicion in range(1, len(turnosPaciente) + 1):
            opcionesValidas.append(str(posicion))

        opcion = input(
            "Ingrese el número del turno que desea modificar: \n"
        )

        while opcion not in opcionesValidas:
            print("Opción incorrecta")
            opcion = input("Seleccione nuevamente el turno: \n ")

        #Convertimos la opción después de comprobar que corresponde a uno de los turnos mostrados
        opcion = int(opcion)

        #Restamos uno porque las posiciones de la lista empiezan en 0
        turnoReprogramar = turnosPaciente[opcion - 1]

        #Conservamos el profesional del turno original
        legajoProfesional = turnoReprogramar[1]

        #Solicitamos una fehca y hora nueva hasta que todas las comprobaciones sean válidas
        nuevoTurnoValido = False

        while not nuevoTurnoValido:
            fecha,hora = ingresarFechaHora()

            #Comprovamos que la fecha y hora nueva pertenecen al horario de atención del profesional
            horarioValido = validarHorarioProfesional(profesionales, legajoProfesional, fecha, hora)

            if not horarioValido:
                diaSemana = obtenerDiaSemana(fecha)

                print("El profesional no atiende ese día o a esa hora")

                print("Horario del " + diaSemana + ": " + Profesionales.getHorarioProfesional(profesionales, legajoProfesional, diaSemana))
            else:

                #Comprobamos por separado la disponibilidad del profesional y del paciente
                horarioOcupado = False
                pacienteOcupado = False


                for turno in turnos:
                    #No se compara el turno consigo mismo, se comprueba si el profesional ya está ocupado
                    if (
                        turno != turnoReprogramar
                        and turno[1] == turnoReprogramar[1]
                        and turno[2] == fecha
                        and turno[3] == hora
                    ):
                        horarioOcupado = True

                    #También comprobamos que el paciente no tenga otro turno en la fecha y hora nueva
                    if(
                        turno != turnoReprogramar
                        and turno[0] == legajoPaciente
                        and turno[2] == fecha
                        and turno[3] == hora
                    ):
                        pacienteOcupado = True
                if horarioOcupado:
                    print(
                        "El profesional ya tiene un turno esa fecha y hora, elija otro horario \n"
                    )
                elif pacienteOcupado:
                    print("El paciente ya tiene otro turno en esa fecha y hora")
                else:
                    #la nueva fecha y hora son correctas, así que finalizamos el bucle
                    nuevoTurnoValido = True

                    #Modificamos directamente la fecha y hora del turno seleccionado
                    turnoReprogramar[2] = fecha
                    turnoReprogramar[3] = hora

                    print("Turno reprogramado correctamente \n")

#Cancela uno de los turnos asignados al legajo de un paciente
def cancelarTurno(turnos):
    if not turnos:
        print("No hay turnos registrados en el sistema. \n")
        return
    
    legajoPaciente = input("Ingrese el legajo del paciente: ")

    #Guardamos únicamente los turnos del paciente indicado
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
            print("Legajo del paciente: " + turno[0])
            print("Legajo del profesional: " + turno[1])
            print("Fecha: " + turno[2])
            print("Hora: " + turno[3])
            print()