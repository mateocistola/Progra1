import Especialidades
from datetime import datetime, timedelta

#Comprueba que una hora tenga el formato HH:MM y que
#las horas y los minutos estén dentro de los valores permitidos
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

#Comprueba que las dos horas sean válidas y que la hora
#de inicio sea anterior a la hora de finalización
def validarRangoHorario(horaInicio, horaFin):
    rangoValido = False

    if validarHora(horaInicio) and validarHora(horaFin):
        partesInicio = horaInicio.split(":")
        partesFin = horaFin.split(":")

#Convertimos las horas completadas a minutos para poder comparar
        #fácilmente el comienzo y el final
        minutosInicio = (int(partesInicio[0])* 60 + int(partesInicio[1]))

        minutosFin = int(partesFin[0])* 60 + int(partesFin[1])

        if minutosInicio < minutosFin:
            rangoValido = True
    return rangoValido

#Busca un profesional por su legajo utilizando recursividad
#La posición indica el profesional que se está comprobando
def buscarProfesionalPorLegajo(profesionales, legajo, posicion = 0):

    #Como base: se llegó al final sin encontrar el legajo
    if posicion == len(profesionales):
        profesionalEncontrado = None
    #El profesional de la posición actual tiene el legajo buscado
    elif profesionales[posicion][0] == legajo:
        profesionalEncontrado = profesionales[posicion]
    #Caso recursivo, se continúa buscando en la siguiente posición
    else:
        profesionalEncontrado = buscarProfesionalPorLegajo(profesionales, legajo, posicion + 1)

    return profesionalEncontrado

#Busca todos los profesionales que pertenecen a una especialidad

def buscarProfesionalesPorEspecialidad(profesionales, especialidad):
    profesionalEncontrados = []

    for profesional in profesionales:
        if profesional[2].lower() == especialidad.lower():
            profesionalEncontrados.append(profesional)
    return profesionalEncontrados
#Devuelve el horario de un profesional para un día concreto, si la lista del día está vacía, significa que no atiende.
#Para sacar el horario del profesional que se está sacando turno, chequeamos el id y evitamos reescribir.
def getHorarioProfesional(profesionales, legajo, dia):
    horario = None

    for profesional in profesionales:
        if profesional[0] == legajo:
            horarios = profesional[3]

            if dia in horarios:
                horarioDia = horarios[dia]

                if horarioDia:
                    horario = horarioDia[0] + " a " + horarioDia[1] + " hs"
                else:
                    horario = "No atiende"
    return horario


#para chequear si el profesional tiene turnos asignados, es util por ejemplo al momento de eliminar un profesional, primero chequear si tiene turnos
def tieneTurnos(turnos, legajo):
    tieneTurnosAsignados = False

    for turno in turnos:
    #La posición 1 contiene el legajo del profesional
        if turno[1] == legajo:
            tieneTurnosAsignados = True
            break #cortamos el bucle porque ya encontramos un turno asignado y no hace falta seguir recorriendo la lista
    return tieneTurnosAsignados

#Muestra los datos de todos los profesionales junto con sus horarios de atención
#para cada día de la semana
def mostrarProfesionales(profesionales):
    print("Los profesionales disponibles son: ")

    for profesional in profesionales:
        print("Legajo: " + profesional[0])
        print("Nombre: " + profesional[1])
        print("Especialidad: " + profesional[2])
        print("Duración de cada turno: " + str(profesional[4]) + " minutos")
        print(" Horario:")

        #La petición 3 contiene el diccionario de horarios
        horarios = profesional[3]

        #Recorremos el diccionario para mostrar el horario correspondiente a cada día
        for dia in horarios:

            #Una lista con dos elementos contiene la hora de inicio y la hora de finalización
            if horarios[dia]:
                print(dia + ": " + horarios[dia][0] + " a " + horarios[dia][1] + " hs")
            else:
                #Una lista vacía indica que ese día no se atiende
                print(dia + ": No atiende")

        print()


#Solicita un legajo, busca el profesional de forma recursiva y muestra sus datos y horarios si existe
def mostrarProfesionalPorLegajo(profesionales):
    legajo = input("Ingrese el legajo del profesional: ")

    #Utilizamos la función recursiva para realizar la búsqueda
    profesionalEncontrado = buscarProfesionalPorLegajo(profesionales, legajo)

    #Si la búsqueda devuelve None, el legajo no está registrado
    if profesionalEncontrado is None:
        print("No se encontró un profesional con el legajo ingresado")
    else:
        print("Legajo: " + profesionalEncontrado[0])
        print("Nombre: " + profesionalEncontrado[1])
        print("Especialidad: " + profesionalEncontrado[2])
        print("Duración de cada turno: " + str(profesionalEncontrado[4]) + " minutos")
        print("Cantidad de sobreturnos: " + str(profesionalEncontrado[5]))
        print("Horarios: ")


        #Mostramos los horarios guardados en la posición 3
        horarios = profesionalEncontrado[3]

        for dia in horarios:
            if horarios[dia]:
                print(dia + ": " + horarios[dia][0] + " a " + horarios[dia][1] + " hs ")
            else:
                print(dia + ": No atiende")


def menu(profesionales, turnos, especialidades):
    eleccion = 0

    while eleccion != 6:
        eleccion = input(
            "Gestión de profesionales, ingrese: \n"
            "1 para agregar un profesional. \n"
            "2 para quitar un profesional. \n"
            "3 para modificar un profesional. \n"
            "4 para modificar el horario de un profesional. \n"
            "5 para buscar un profesional por legajo. \n"
            "6 para salir al menú principal. \n"
        )

        while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > 6:
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 6: ")

        eleccion = int(eleccion)

        match eleccion:
            case 1:
                agregarProfesionales(profesionales, especialidades)
            case 2:
                quitarProfesionales(profesionales, turnos)
            case 3:
                editarProfesionales(profesionales, especialidades, turnos)
            case 4:
                modificarHorario(profesionales)
            case 5:
                mostrarProfesionalPorLegajo(profesionales)
            case 6:
                print("Volvemos al menú principal")

   

#Permite modificar el horario de un profesional para un día concreto o indicar que ese día no atiende.
def modificarHorario(profesionales):
    legajo = input("Ingrese el legajo del profesional: ")

    profesionalEncontrado = []

    for profesional in profesionales:
        if profesional[0] == legajo:
            profesionalEncontrado = profesional
            break #cortamos el bucle porque ya encontramos el profesional y no hace falta seguir recorriendo la lista
    if profesionalEncontrado:
        #Recuperamos el diccionario completo de horarios
        horarios = profesionalEncontrado[3]

        print("Días disponibles: ")

        for dia in horarios:
            print(dia)

        dia = input("Ingrese el día que deseas modificar: ")
        #El día introducido debe existir como clave del diccionario
        while dia not in horarios:
            print("Día incorrecto")
            dia = input("Ingrese nuevamente el día: ")

        print("Horario actual: " + getHorarioProfesional(profesionales, legajo, dia))

        #Si no atiende, guardaremos una lista vacía para ese día
        atiende = input("¿El profesional atiende ese día? Ingrese s o n: ")

        while atiende != "s" and atiende != "n":
            print("Opción incorrecta")
            atiende = input("Ingrese s o n")
        if atiende == "s":
            horaInicio = input("Ingrese nuevo horario de comienzo de atención: ")
            horaFin = input("Ingrese nuevo horario de fin de atención: ")

            #Volvemos a solicitar las horas para obtener un rango válido
            while not validarRangoHorario(horaInicio,horaFin):
                print("Horario inválido")
                horaInicio = input("Ingrese nuevamente la hora de inicio: ")
                horaFin = input("Ingrese nuevamente la hora de fin: ")
            #Sustituimos únicamente el horario del día elegido
            horarios[dia] = [horaInicio, horaFin]
        else:
            #La lista vacía representa un día sin atención.
            horarios[dia] = []

        print("Horario modificado")
    else:
        print("No se encontró un profesional con el legajo ingresado")



def editarProfesionales(profesionales, especialidades, turnos):
    mostrarProfesionales(profesionales)

    legajo = input("Ingrese legajo del profesional para editar: ")

    profesionalEncontrado = []

    for profesional in profesionales:
        if profesional[0] == legajo:
            profesionalEncontrado = profesional
            break #cortamos el bucle porque ya encontramos el profesional y no hace falta seguir recorriendo la lista

    if profesionalEncontrado:
        print("Nombre actual: " + profesionalEncontrado[1])

        nombre = input(
                "Ingrese nuevo nombre: o  enter para mantener el nombre actual: "
        )

        if nombre == "":
                nombre = profesionalEncontrado[1]

        print("Especialidad actual: " + profesionalEncontrado[2])
        Especialidades.listarEspecialidades(especialidades)
        especialidad = input(
                    "Ingrese nueva especialidad: o bien presione enter "
                    "para mantener la especialidad actual: "
        )

        if especialidad == "":
                especialidad = profesionalEncontrado[2]
        else:
            while not Especialidades.especialidadRegistrada(especialidades, especialidad):
                print("La especialidad ingresada no está registrada")
                especialidad = input("Ingrese de nuevo la especialidad: ")
            # Guardamos el nombre tal y como aparece registrado
            for nombreEspecialidad in especialidades:
                if nombreEspecialidad.lower() == especialidad.lower():
                    especialidad = nombreEspecialidad
        print("Duración actual de los turnos: " + str(profesionalEncontrado[4]) + " minutos")
        duracionTurno = input("Ingrese la nueva duración o presione enter para mantener la duración actual: ")
        if duracionTurno == "":
            duracionTurno = profesionalEncontrado[4]
        elif tieneTurnos(turnos, legajo):
            print("No se puede modificar la duración porque el profesional tiene turnos asignados")
            duracionTurno = profesionalEncontrado[4]
        else:
            while(not duracionTurno.isdigit() or int(duracionTurno) <= 0 ):
                print("La duración debe ser un número mayor que cero")
                duracionTurno = input("Ingrese nuevamente la duración en minutos: ")
            duracionTurno = int(duracionTurno)
        print("Sobreturnos actuales: " + str(profesionalEncontrado[5]))

        cantidadSobreturnos = input(
            "Ingrese la nueva cantidad de sobreturnos o presione enter para mantener la actual: "
        )

        if cantidadSobreturnos != "":
            while not cantidadSobreturnos.isdigit():
                print("Ingrese un número válido")
                cantidadSobreturnos = input("Ingrese nuevamente la cantidad: ")

        profesionalEncontrado[1] = nombre
        profesionalEncontrado[2] = especialidad
        profesionalEncontrado[4] = duracionTurno
        profesionalEncontrado[5] = int(cantidadSobreturnos)

        print("Profesional  modificado")
    else:

       print("No se encontró un profesional con el legajo ingresado")


#Registra un nuevo profesional y solicita sus horarios de atención para cada día de la semana
def agregarProfesionales(profesionales, especialidades):
    mostrarProfesionales(profesionales)

    if not especialidades:
        print("No se pueden añadir profesionales porque no hay especialidades registradas")
        return

    legajo = input("Ingrese legajo del profesional para agregar: ")
    #Comprobamos que no exista otro profesional con el mismo legajo
    legajoRegistrado = False

    for profesional in profesionales:
        if profesional[0] == legajo:
            legajoRegistrado = True
    if legajoRegistrado:
        print("Ya existe un profesional con ese legajo")
    else:
        nombre = input("Ingrese nombre del profesional: ")
        Especialidades.listarEspecialidades(especialidades)
        especialidad = input("Ingrese especialidad del profesional: ")
        while not Especialidades.especialidadRegistrada(especialidades,especialidad):
            print("La especialidad ingresada no está registrada")
            especialidad = input("Ingrese de nuevo la especialidad: ")
        for nombreEspecialidad in especialidades:
            if nombreEspecialidad.lower() == especialidad.lower():
                especialidad = nombreEspecialidad
                break #cortamos el bucle porque ya encontramos la especialidad y no hace falta seguir recorriendo la lista

        #Solicitamos la duración de los turnos del profesional
        duracionTurno = input("Ingrese la duración de cada turno en minutos: ")

        while not duracionTurno.isdigit() or int(duracionTurno) <= 0:
            print("La duración debe ser un número mayor que cero")
            duracionTurno = input("Ingrese nuevamente la duración en minutos: ")

        duracionTurno = int(duracionTurno)

        #Esta lista se utiliza para solicitar el horario de todos los días de la semana
        dias = ["lunes","martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        #El diccionario relaciona cada día con su rango horario
        horarios = {}
        #Solicitamos el horario de atención de cada día
        for dia in dias:
            atiende = input("¿El profesional atiende el " + dia + "? Ingrese s o n: ")

            while atiende != "s" and atiende != "n":
                print("Opción incorrecta")
                atiende = input("Ingrese s o n")

            if atiende == "s":
                horaInicio = input("Ingrese horario de comienzo con formato HH:MM: ")
                horaFin = input("Ingrese horario de fin con formato HH:MM: ")

                #Las horas se vuelve a solicitar si el formato o el orden del rango no son válidos
                while not validarRangoHorario(horaInicio, horaFin):
                    print("Horario invalido")
                    horaInicio = input("Ingrese nuevamente la hora de inicio: ")
                    horaFin = input("Ingrese nuevamente la hora de fin: ")

                #Guardamos la hora de inicio y de fin del día
                horarios[dia] = [horaInicio, horaFin]
                #nuevo cantidad de sobreturnos 
                cantidadSobreturnos = input("Ingrese la cantidad de sobreturnos permitidos: ")

                while not cantidadSobreturnos.isdigit():
                    print("Ingrese un número válido")
                    cantidadSobreturnos = input("Ingrese nuevamente la cantidad: ")

                cantidadSobreturnos = int(cantidadSobreturnos)
            else:
                #Si no atiende, se guarda una lista vacía
                horarios[dia] = []
        #Añadimos el profesional con todos sus datos y horarios.
        profesionales.append([
            legajo,
            nombre,
            especialidad,
            horarios,
            duracionTurno,
            cantidadSobreturnos
        ])

        print("Profesional agregado correctamente")

#Elimina un profesional solamente si no tiene turnos asignados
def quitarProfesionales(profesionales, turnos):
    mostrarProfesionales(profesionales)

    legajo = input("Ingrese el legajo del profesional a quitar: ")
    #Primero comprobamos que sus turnos hayan sido cancelados
    if tieneTurnos(turnos, legajo):
        print("No se puede eliminar el profesional porque tiene turnos asignados, cancele primero los turnos.")

    else:
        #Guardamos el profesional encontrado para eliminarlo después de terminar el recorrido

        profesionalesEliminar = []

        for profesional in profesionales:
            if profesional[0] == legajo:
                profesionalesEliminar = profesional
                break

        if profesionalesEliminar:
            #Eliminamoos de la lista el profesional encontrado
            profesionales.remove(profesionalesEliminar)
            print("Profesional eliminado")
        else:

            print("No se encontró un profesional con el legajo ingresado.")


# Busca el primer profesional de una especialidad que tenga disponible
# una fecha y hora determinada
def buscarPrimerProfesionalConTurnoLibre(profesionales, turnos, especialidad, dia, fecha, hora):

    profesionalDisponible = None

    for profesional in profesionales:

        if profesional[2].lower() == especialidad.lower():

            horarios = profesional[3]

            if dia in horarios and horarios[dia]:

                horaInicio = horarios[dia][0]
                horaFin = horarios[dia][1]

                partesInicio = horaInicio.split(":")
                partesFin = horaFin.split(":")
                partesHora = hora.split(":")

                minutosInicio = int(partesInicio[0]) * 60 + int(partesInicio[1])
                minutosFin = int(partesFin[0]) * 60 + int(partesFin[1])
                minutosHora = int(partesHora[0]) * 60 + int(partesHora[1])

                duracion = profesional[4]

                # Comprobamos que el turno entre en el horario de atención
                if (minutosInicio <= minutosHora and
                    minutosHora + duracion <= minutosFin and
                    (minutosHora - minutosInicio) % duracion == 0):

                    ocupado = False

                    for turno in turnos:

                        if (turno[1] == profesional[0] and
                            turno[2] == fecha and
                            turno[3] == hora):

                            ocupado = True
                            break

                    if not ocupado:
                        profesionalDisponible = profesional
                        break

    return profesionalDisponible

# Busca el primer turno disponible desde la fecha actual
# considerando los horarios y los sobreturnos de cada profesional
def buscarPrimerTurnoLibre(profesionales, turnos, especialidad, dni, turnoExcluir=None):

    diasSemana = ["lunes", "martes", "miércoles", "jueves",
                  "viernes", "sábado", "domingo"]

    hayHorarios = False

    for profesional in profesionales:
        if profesional[2].lower() == especialidad.lower():
            for dia in profesional[3]:
                if profesional[3][dia]:
                    hayHorarios = True

    if not hayHorarios:
        return None

    fechaActual = datetime.now().date()
    horaActual = datetime.now().hour * 60 + datetime.now().minute

    while True:

        diaSemana = diasSemana[fechaActual.weekday()]
        fecha = fechaActual.strftime("%d/%m/%Y")

        profesionalDisponible = None
        horaDisponible = None
        sobreTurnoDisponible = False
        mejorHorario = 1440

        for profesional in profesionales:

            if profesional[2].lower() == especialidad.lower():

                horarios = profesional[3]

                if diaSemana in horarios and horarios[diaSemana]:

                    horaInicio = horarios[diaSemana][0]
                    horaFin = horarios[diaSemana][1]

                    partesInicio = horaInicio.split(":")
                    partesFin = horaFin.split(":")

                    minutosInicio = int(partesInicio[0]) * 60 + int(partesInicio[1])
                    minutosFin = int(partesFin[0]) * 60 + int(partesFin[1])

                    duracion = profesional[4]

                    # Buscamos primero dentro del horario habitual
                    minutos = minutosInicio

                    while minutos + duracion <= minutosFin:

                        if fechaActual > datetime.now().date() or minutos > horaActual:

                            hora = str(minutos // 60).zfill(2) + ":" + str(minutos % 60).zfill(2)

                            ocupado = False

                            # Evitamos ofrecer nuevamente el mismo turno que se está reprogramando
                            if turnoExcluir is not None and turnoExcluir[2] == fecha and turnoExcluir[3] == hora:
                                ocupado = True

                            for turno in turnos:
                                if turno is not turnoExcluir and ((turno[1] == profesional[0] or turno[0] == dni)
                                    and turno[2] == fecha
                                    and turno[3] == hora):
                                    ocupado = True
                                    break

                            if not ocupado and minutos < mejorHorario:
                                mejorHorario = minutos
                                profesionalDisponible = profesional
                                horaDisponible = hora
                                sobreTurnoDisponible = False

                        minutos += duracion

                    # Si no hay lugar en el horario habitual, buscamos sobreturnos
                    for numero in range(profesional[5]):

                        minutos = minutosFin + numero * duracion

                        if minutos + duracion <= 1440:

                            if fechaActual > datetime.now().date() or minutos > horaActual:

                                hora = str(minutos // 60).zfill(2) + ":" + str(minutos % 60).zfill(2)

                                ocupado = False

                                if turnoExcluir is not None and turnoExcluir[2] == fecha and turnoExcluir[3] == hora:
                                    ocupado = True

                                for turno in turnos:
                                    if turno is not turnoExcluir and ((turno[1] == profesional[0] or turno[0] == dni)
                                        and turno[2] == fecha
                                        and turno[3] == hora):
                                        ocupado = True
                                        break

                                if not ocupado and minutos < mejorHorario:
                                    mejorHorario = minutos
                                    profesionalDisponible = profesional
                                    horaDisponible = hora
                                    sobreTurnoDisponible = True

        if profesionalDisponible is not None:
            return (profesionalDisponible, fecha, horaDisponible, sobreTurnoDisponible)

        fechaActual = fechaActual + timedelta(days=1)
# Busca un profesional disponible para una fecha y hora seleccionadas
def buscarProfesionalParaFechaHora(profesionales, turnos, especialidad, dni, dia, fecha, hora, turnoExcluir=None):

    partesHora = hora.split(":")
    minutosHora = int(partesHora[0]) * 60 + int(partesHora[1])

    for profesional in profesionales:

        if profesional[2].lower() == especialidad.lower():

            horarios = profesional[3]

            if dia in horarios and horarios[dia]:

                partesInicio = horarios[dia][0].split(":")
                partesFin = horarios[dia][1].split(":")

                minutosInicio = int(partesInicio[0]) * 60 + int(partesInicio[1])
                minutosFin = int(partesFin[0]) * 60 + int(partesFin[1])

                duracion = profesional[4]
                horarioValido = False

                # Comprobamos si pertenece al horario habitual
                if (minutosInicio <= minutosHora and
                    minutosHora + duracion <= minutosFin and
                    (minutosHora - minutosInicio) % duracion == 0):

                    horarioValido = True

                # Comprobamos si corresponde a un sobreturno
                for numero in range(profesional[5]):

                    if minutosHora == minutosFin + numero * duracion:
                        horarioValido = True

                if horarioValido:

                    ocupado = False

                    # Evitamos seleccionar nuevamente el mismo turno original
                    if turnoExcluir is not None and turnoExcluir[2] == fecha and turnoExcluir[3] == hora:
                        ocupado = True

                    for turno in turnos:

                        if turno is not turnoExcluir and ((turno[1] == profesional[0] or turno[0] == dni)
                            and turno[2] == fecha
                            and turno[3] == hora):

                            ocupado = True
                            break

                    if not ocupado:
                        return profesional

    return None