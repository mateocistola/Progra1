import Especialidades

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
        print("Horarios: ")

        #Mostramos los horarios guardados en la posición 3
        horarios = profesionalEncontrado[3]

        for dia in horarios:
            if horarios[dia]:
                print(dia + ": " + horarios[dia][0] + " a " + horarios[dia][1] + " hs ")
            else:
                print(dia + ": No atiende")


def menu(profesionales, turnos, especialidades):


    eleccion = int(input(
        "Gestión de profesionales, ingrese: \n"
        "1 para agregar un profesional. \n"
        "2 para quitar un profesional. \n"
        "3 para modificar un profesional. \n"
        "4 para modificar el horario de un profesional. \n"
        "5 para buscar un profesional por legajo. \n"
        "6 para salir al menú principal. \n"
    ))

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
        case _:
            print("Opción incorrecta.")

   

#Permite modificar el horario de un profesional para un día concreto o indicar que ese día no atiende.
def modificarHorario(profesionales):
    legajo = input("Ingrese el legajo del profesional: ")

    profesionalEncontrado = []

    for profesional in profesionales:
        if profesional[0] == legajo:
            profesionalEncontrado = profesional

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

       profesionalEncontrado[1] = nombre
       profesionalEncontrado[2] = especialidad
       profesionalEncontrado[4] = duracionTurno

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
        #Solicitamos la duración de los turnos del profesional
        duracionTurno = input("Ingrese la duración de cada turno en minutos: ")
        while(not duracionTurno.isdigit() or int(duracionTurno) <= 0):
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
            else:
                #Si no atiende, se guarda una lista vacía
                horarios[dia] = []

        #Añadimos el profesional con todos sus datos y horarios.
        profesionales.append([
            legajo,
            nombre,
            especialidad,
            horarios,
            duracionTurno
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

        if profesionalesEliminar:
            #Eliminamoos de la lista el profesional encontrado
            profesionales.remove(profesionalesEliminar)
            print("Profesional eliminado")
        else:

            print("No se encontró un profesional con el legajo ingresado.")

