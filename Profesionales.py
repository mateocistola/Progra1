import os
from datetime import datetime, timedelta
import Especialidades


ARCHIVO_PROFESIONALES = "profesionales.txt"
ARCHIVO_TURNOS = "turnos.txt"
ARCHIVO_AUXILIAR = "profesionales_aux.txt"

diasSemana = [
    "lunes", "martes", "miércoles", "jueves",
    "viernes", "sábado", "domingo"
]


# Convierte una línea del archivo en un único profesional.
# Estructura: [legajo, nombre, especialidad, horarios, duracion, sobreturnos]
def convertirProfesional(linea):
    datos = linea.rstrip("\n").split(";")

    if len(datos) != 19:
        raise ValueError("El registro del profesional no tiene 19 campos")

    horarios = {}
    posicion = 5

    for dia in diasSemana:
        horaInicio = datos[posicion]
        horaFin = datos[posicion + 1]

        if horaInicio == "-" and horaFin == "-":
            horarios[dia] = []
        else:
            horarios[dia] = [horaInicio, horaFin]

        posicion += 2

    return [
        datos[0], datos[1], datos[2], horarios,
        int(datos[3]), int(datos[4])
    ]


# Convierte un profesional en una línea para guardarlo en el archivo.
def convertirLinea(profesional):
    datos = [
        profesional[0],
        profesional[1],
        profesional[2],
        str(profesional[4]),
        str(profesional[5])
    ]

    horarios = profesional[3]

    for dia in diasSemana:
        if horarios[dia]:
            datos.append(horarios[dia][0])
            datos.append(horarios[dia][1])
        else:
            datos.append("-")
            datos.append("-")

    return ";".join(datos) + "\n"


# Busca un profesional por legajo leyendo el archivo secuencialmente.
def buscarProfesionalPorLegajo(legajo):
    profesionalEncontrado = None
    archivo = None

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt")
        linea = archivo.readline()

        while linea != "" and profesionalEncontrado is None:
            profesional = convertirProfesional(linea)

            if profesional[0] == str(legajo):
                profesionalEncontrado = profesional
            else:
                linea = archivo.readline()

    except FileNotFoundError:
        print("Todavía no existe el archivo de profesionales.")
    except (OSError, ValueError) as mensaje:
        print("No se pudo leer el archivo de profesionales:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return profesionalEncontrado


# Comprueba si existe algún profesional de una especialidad.
def existeProfesionalPorEspecialidad(especialidad):
    existe = False
    archivo = None

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt")
        linea = archivo.readline()

        while linea != "" and not existe:
            profesional = convertirProfesional(linea)

            if profesional[2].lower() == especialidad.lower():
                existe = True

            linea = archivo.readline()

    except FileNotFoundError:
        print("Todavía no existe el archivo de profesionales.")
    except (OSError, ValueError) as mensaje:
        print("No se pudo leer el archivo de profesionales:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return existe


# Valida el formato HH:MM y los valores de horas y minutos.
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


# Comprueba que el inicio sea anterior al fin.
def validarRangoHorario(horaInicio, horaFin):
    rangoValido = False

    if validarHora(horaInicio) and validarHora(horaFin):
        partesInicio = horaInicio.split(":")
        partesFin = horaFin.split(":")

        minutosInicio = int(partesInicio[0]) * 60 + int(partesInicio[1])
        minutosFin = int(partesFin[0]) * 60 + int(partesFin[1])

        if minutosInicio < minutosFin:
            rangoValido = True

    return rangoValido


# Devuelve el horario de un profesional para un día concreto.
def getHorarioProfesional(legajo, dia):
    horario = None
    profesional = buscarProfesionalPorLegajo(legajo)

    if profesional is not None and dia in profesional[3]:
        horarioDia = profesional[3][dia]

        if horarioDia:
            horario = horarioDia[0] + " a " + horarioDia[1] + " hs"
        else:
            horario = "No atiende"

    return horario


# Comprueba si un profesional tiene turnos asignados.
# Lee turnos.txt de a una línea, sin cargar todos los turnos.
def tieneTurnos(legajo):
    tieneTurnosAsignados = False
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt")
        linea = archivo.readline()

        while linea != "" and not tieneTurnosAsignados:
            datos = linea.rstrip("\n").split(";")

            if len(datos) == 4 and datos[1] == str(legajo):
                tieneTurnosAsignados = True
            else:
                linea = archivo.readline()

    except FileNotFoundError:
        tieneTurnosAsignados = False
    except OSError as mensaje:
        print("No se pudo leer el archivo de turnos:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return tieneTurnosAsignados


# Muestra los profesionales leyendo el archivo registro por registro.
def mostrarProfesionales():
    archivo = None
    hayProfesionales = False

    print("Los profesionales disponibles son:")

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt")
        linea = archivo.readline()

        while linea != "":
            profesional = convertirProfesional(linea)
            hayProfesionales = True

            print("Legajo: " + profesional[0])
            print("Nombre: " + profesional[1])
            print("Especialidad: " + profesional[2])
            print("Duración de cada turno: " + str(profesional[4]) + " minutos")
            print("Cantidad de sobreturnos: " + str(profesional[5]))
            print("Horario:")

            for dia in diasSemana:
                if profesional[3][dia]:
                    print(dia + ": " + profesional[3][dia][0] +
                          " a " + profesional[3][dia][1] + " hs")
                else:
                    print(dia + ": No atiende")

            print()
            linea = archivo.readline()

        if not hayProfesionales:
            print("No hay profesionales registrados.")

    except FileNotFoundError:
        print("Todavía no hay profesionales registrados.")
    except (OSError, ValueError) as mensaje:
        print("No se pudo leer el archivo de profesionales:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()


# Muestra los profesionales que atienden el día actual.
def mostrarProfesionalesDelDia():
    archivo = None
    diaActual = diasSemana[datetime.now().weekday()]
    hayProfesionales = False

    print("Los profesionales que atienden hoy (" + diaActual + ") son:")

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt")
        linea = archivo.readline()

        while linea != "":
            profesional = convertirProfesional(linea)

            if profesional[3][diaActual]:
                hayProfesionales = True
                print("Legajo: " + profesional[0])
                print("Nombre: " + profesional[1])
                print("Especialidad: " + profesional[2])
                print("Duración de cada turno: " +
                      str(profesional[4]) + " minutos")
                print()

            linea = archivo.readline()

        if not hayProfesionales:
            print("No hay profesionales que atiendan hoy.")

    except FileNotFoundError:
        print("Todavía no hay profesionales registrados.")
    except (OSError, ValueError) as mensaje:
        print("No se pudo leer el archivo de profesionales:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()


# Solicita un legajo, busca el profesional y muestra sus datos.
def mostrarProfesionalPorLegajo():
    legajo = input("Ingrese el legajo del profesional: ")
    profesionalEncontrado = buscarProfesionalPorLegajo(legajo)

    if profesionalEncontrado is None:
        print("No se encontró un profesional con el legajo ingresado.")
    else:
        print("Legajo: " + profesionalEncontrado[0])
        print("Nombre: " + profesionalEncontrado[1])
        print("Especialidad: " + profesionalEncontrado[2])
        print("Duración de cada turno: " +
              str(profesionalEncontrado[4]) + " minutos")
        print("Cantidad de sobreturnos: " +
              str(profesionalEncontrado[5]))
        print("Horarios:")

        for dia in diasSemana:
            if profesionalEncontrado[3][dia]:
                print(dia + ": " + profesionalEncontrado[3][dia][0] +
                      " a " + profesionalEncontrado[3][dia][1] + " hs")
            else:
                print(dia + ": No atiende")


# Reescribe el archivo auxiliarmente para modificar o eliminar un registro.
# No mantiene una colección de profesionales en memoria.
def _reescribirProfesionales(legajo, profesionalNuevo=None):
    archivoOriginal = None
    archivoAuxiliar = None
    encontrado = False
    operacionCorrecta = False

    try:
        archivoOriginal = open(ARCHIVO_PROFESIONALES, "rt")
        archivoAuxiliar = open(ARCHIVO_AUXILIAR, "wt")

        linea = archivoOriginal.readline()

        while linea != "":
            profesional = convertirProfesional(linea)

            if profesional[0] == str(legajo):
                encontrado = True

                if profesionalNuevo is not None:
                    archivoAuxiliar.write(convertirLinea(profesionalNuevo))
            else:
                archivoAuxiliar.write(linea)

            linea = archivoOriginal.readline()

        archivoOriginal.close()
        archivoOriginal = None
        archivoAuxiliar.close()
        archivoAuxiliar = None

        if encontrado:
            os.remove(ARCHIVO_PROFESIONALES)
            os.rename(ARCHIVO_AUXILIAR, ARCHIVO_PROFESIONALES)
            operacionCorrecta = True
        else:
            os.remove(ARCHIVO_AUXILIAR)

    except FileNotFoundError:
        print("No existe el archivo de profesionales.")
    except (OSError, ValueError) as mensaje:
        print("No se pudo actualizar el archivo de profesionales:", mensaje)
    finally:
        if archivoOriginal is not None:
            archivoOriginal.close()
        if archivoAuxiliar is not None:
            archivoAuxiliar.close()

    return operacionCorrecta


# Actualiza una especialidad en todos los profesionales que la tengan asignada.
# Reescribe el archivo secuencialmente mediante un archivo auxiliar.
def actualizarEspecialidadProfesionales(nombreActual, nombreNuevo):
    archivoOriginal = None
    archivoAuxiliar = None
    encontrado = False
    correcto = False

    try:
        archivoOriginal = open(ARCHIVO_PROFESIONALES, "rt")
        archivoAuxiliar = open(ARCHIVO_AUXILIAR, "wt")
        linea = archivoOriginal.readline()

        while linea != "":
            profesional = convertirProfesional(linea)

            if profesional[2].lower() == nombreActual.lower():
                profesional[2] = nombreNuevo
                encontrado = True
                archivoAuxiliar.write(convertirLinea(profesional))
            else:
                archivoAuxiliar.write(linea)

            linea = archivoOriginal.readline()

        archivoOriginal.close()
        archivoOriginal = None
        archivoAuxiliar.close()
        archivoAuxiliar = None

        if encontrado:
            os.remove(ARCHIVO_PROFESIONALES)
            os.rename(ARCHIVO_AUXILIAR, ARCHIVO_PROFESIONALES)
        else:
            os.remove(ARCHIVO_AUXILIAR)

        correcto = True

    except FileNotFoundError:
        correcto = True
    except (OSError, ValueError) as mensaje:
        print("No se pudo actualizar la especialidad de los profesionales:", mensaje)
    finally:
        if archivoOriginal is not None:
            archivoOriginal.close()
        if archivoAuxiliar is not None:
            archivoAuxiliar.close()

    return correcto


# Menú de gestión de profesionales.
def menu():
    eleccion = 0

    while eleccion != 6:
        eleccion = input(
            "Gestión de profesionales, ingrese:\n"
            "1 para agregar un profesional.\n"
            "2 para quitar un profesional.\n"
            "3 para modificar un profesional.\n"
            "4 para modificar el horario de un profesional.\n"
            "5 para buscar un profesional por legajo.\n"
            "6 para salir al menú principal.\n"
        )

        while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > 6:
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 6: ")

        eleccion = int(eleccion)

        match eleccion:
            case 1:
                agregarProfesionales()
            case 2:
                quitarProfesionales()
            case 3:
                editarProfesionales()
            case 4:
                modificarHorario()
            case 5:
                mostrarProfesionalPorLegajo()
            case 6:
                print("Volvemos al menú principal.")


# Modifica el horario de un día y guarda el profesional en el archivo.
def modificarHorario():
    legajo = input("Ingrese el legajo del profesional: ")
    profesionalEncontrado = buscarProfesionalPorLegajo(legajo)

    if profesionalEncontrado is None:
        print("No se encontró un profesional con el legajo ingresado.")
        return

    horarios = profesionalEncontrado[3]

    print("Días disponibles:")
    for dia in diasSemana:
        print(dia)

    dia = input("Ingrese el día que desea modificar: ").lower()

    while dia not in horarios:
        print("Día incorrecto.")
        dia = input("Ingrese nuevamente el día: ").lower()

    print("Horario actual: " + getHorarioProfesional(legajo, dia))

    atiende = input("¿El profesional atiende ese día? Ingrese s o n: ").lower()

    while atiende != "s" and atiende != "n":
        print("Opción incorrecta.")
        atiende = input("Ingrese s o n: ").lower()

    if atiende == "s":
        horaInicio = input("Ingrese nuevo horario de comienzo de atención: ")
        horaFin = input("Ingrese nuevo horario de fin de atención: ")

        while not validarRangoHorario(horaInicio, horaFin):
            print("Horario inválido.")
            horaInicio = input("Ingrese nuevamente la hora de inicio: ")
            horaFin = input("Ingrese nuevamente la hora de fin: ")

        horarios[dia] = [horaInicio, horaFin]
    else:
        horarios[dia] = []

    if _reescribirProfesionales(legajo, profesionalEncontrado):
        print("Horario modificado correctamente.")


# Modifica los datos generales de un profesional.
def editarProfesionales():
    especialidades = Especialidades.cargarEspecialidades()
    legajo = input("Ingrese legajo del profesional para editar: ")
    profesionalEncontrado = buscarProfesionalPorLegajo(legajo)

    if profesionalEncontrado is None:
        print("No se encontró un profesional con el legajo ingresado.")
        return

    print("Nombre actual: " + profesionalEncontrado[1])
    nombre = input("Ingrese nuevo nombre o presione enter para mantenerlo: ")

    if nombre == "":
        nombre = profesionalEncontrado[1]

    print("Especialidad actual: " + profesionalEncontrado[2])
    Especialidades.listarEspecialidades(especialidades)
    especialidad = input(
        "Ingrese nueva especialidad o presione enter para mantener la actual: "
    )

    if especialidad == "":
        especialidad = profesionalEncontrado[2]
    else:
        while not Especialidades.especialidadRegistrada(
                especialidades, especialidad):
            print("La especialidad ingresada no está registrada.")
            especialidad = input("Ingrese de nuevo la especialidad: ")

        for nombreEspecialidad in especialidades:
            if nombreEspecialidad.lower() == especialidad.lower():
                especialidad = nombreEspecialidad
                break

    print("Duración actual de los turnos: " +
          str(profesionalEncontrado[4]) + " minutos")
    duracionTurno = input(
        "Ingrese la nueva duración o presione enter para mantenerla: "
    )

    if duracionTurno == "":
        duracionTurno = profesionalEncontrado[4]
    elif tieneTurnos(legajo):
        print("No se puede modificar la duración porque tiene turnos asignados.")
        duracionTurno = profesionalEncontrado[4]
    else:
        while not duracionTurno.isdigit() or int(duracionTurno) <= 0:
            print("La duración debe ser un número mayor que cero.")
            duracionTurno = input("Ingrese nuevamente la duración en minutos: ")
        duracionTurno = int(duracionTurno)

    print("Sobreturnos actuales: " + str(profesionalEncontrado[5]))
    cantidadSobreturnos = input(
        "Ingrese la nueva cantidad de sobreturnos o presione enter para mantenerla: "
    )

    if cantidadSobreturnos == "":
        cantidadSobreturnos = profesionalEncontrado[5]
    else:
        while not cantidadSobreturnos.isdigit():
            print("Ingrese un número válido.")
            cantidadSobreturnos = input("Ingrese nuevamente la cantidad: ")
        cantidadSobreturnos = int(cantidadSobreturnos)

    profesionalEncontrado[1] = nombre
    profesionalEncontrado[2] = especialidad
    profesionalEncontrado[4] = duracionTurno
    profesionalEncontrado[5] = cantidadSobreturnos

    if _reescribirProfesionales(legajo, profesionalEncontrado):
        print("Profesional modificado correctamente.")


# Registra un profesional nuevo. Se solicita una sola cantidad de sobreturnos.
def agregarProfesionales():
    especialidades = Especialidades.cargarEspecialidades()
    if not especialidades:
        print("No se pueden añadir profesionales porque no hay especialidades registradas.")
        return

    legajo = input("Ingrese legajo del profesional para agregar: ")

    if buscarProfesionalPorLegajo(legajo) is not None:
        print("Ya existe un profesional con ese legajo.")
        return

    nombre = input("Ingrese nombre del profesional: ")
    Especialidades.listarEspecialidades(especialidades)
    especialidad = input("Ingrese especialidad del profesional: ")

    while not Especialidades.especialidadRegistrada(especialidades, especialidad):
        print("La especialidad ingresada no está registrada.")
        especialidad = input("Ingrese de nuevo la especialidad: ")

    for nombreEspecialidad in especialidades:
        if nombreEspecialidad.lower() == especialidad.lower():
            especialidad = nombreEspecialidad
            break

    duracionTurno = input("Ingrese la duración de cada turno en minutos: ")

    while not duracionTurno.isdigit() or int(duracionTurno) <= 0:
        print("La duración debe ser un número mayor que cero.")
        duracionTurno = input("Ingrese nuevamente la duración en minutos: ")

    duracionTurno = int(duracionTurno)
    horarios = {}

    for dia in diasSemana:
        atiende = input("¿El profesional atiende el " + dia + "? Ingrese s o n: ").lower()

        while atiende != "s" and atiende != "n":
            print("Opción incorrecta.")
            atiende = input("Ingrese s o n: ").lower()

        if atiende == "s":
            horaInicio = input("Ingrese horario de comienzo con formato HH:MM: ")
            horaFin = input("Ingrese horario de fin con formato HH:MM: ")

            while not validarRangoHorario(horaInicio, horaFin):
                print("Horario inválido.")
                horaInicio = input("Ingrese nuevamente la hora de inicio: ")
                horaFin = input("Ingrese nuevamente la hora de fin: ")

            horarios[dia] = [horaInicio, horaFin]
        else:
            horarios[dia] = []

    cantidadSobreturnos = input("Ingrese la cantidad de sobreturnos permitidos: ")

    while not cantidadSobreturnos.isdigit():
        print("Ingrese un número válido.")
        cantidadSobreturnos = input("Ingrese nuevamente la cantidad: ")

    profesional = [
        legajo, nombre, especialidad, horarios,
        duracionTurno, int(cantidadSobreturnos)
    ]

    archivo = None

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "at")
        archivo.write(convertirLinea(profesional))
        print("Profesional agregado correctamente.")
    except OSError as mensaje:
        print("No se pudo guardar el profesional:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()


# Elimina un profesional solamente si no tiene turnos asignados.
def quitarProfesionales():
    legajo = input("Ingrese el legajo del profesional a quitar: ")

    if buscarProfesionalPorLegajo(legajo) is None:
        print("No se encontró un profesional con el legajo ingresado.")
    elif tieneTurnos(legajo):
        print("No se puede eliminar el profesional porque tiene turnos asignados. Cancele primero los turnos.")
    elif _reescribirProfesionales(legajo):
        print("Profesional eliminado correctamente.")


# Convierte HH:MM a minutos desde la medianoche.
def _horaEnMinutos(hora):
    partes = hora.split(":")
    return int(partes[0]) * 60 + int(partes[1])


# Comprueba si una fecha/hora está ocupada por el profesional o por el paciente.
# turnoExcluir es una tupla/lista [dni, legajo, fecha, hora] al reprogramar.
def _turnoOcupado(legajo, dni, fecha, hora, turnoExcluir=None):
    ocupado = False
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt")
        linea = archivo.readline()

        while linea != "" and not ocupado:
            datos = linea.rstrip("\n").split(";")

            if len(datos) == 4:
                esTurnoExcluido = (
                    turnoExcluir is not None and
                    datos[0] == turnoExcluir[0] and
                    datos[1] == turnoExcluir[1] and
                    datos[2] == turnoExcluir[2] and
                    datos[3] == turnoExcluir[3]
                )

                if not esTurnoExcluido:
                    if (datos[1] == str(legajo) or datos[0] == str(dni)):
                        if datos[2] == fecha and datos[3] == hora:
                            ocupado = True

            linea = archivo.readline()

    except FileNotFoundError:
        ocupado = False
    except OSError as mensaje:
        print("No se pudo consultar el archivo de turnos:", mensaje)
        ocupado = True
    finally:
        if archivo is not None:
            archivo.close()

    return ocupado


# Busca un profesional de la especialidad que tenga libre una fecha y hora.
def buscarPrimerProfesionalConTurnoLibre(especialidad, dia, fecha, hora,
                                         dni="", turnoExcluir=None):
    profesionalDisponible = None
    archivo = None

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt")
        linea = archivo.readline()
        minutosHora = _horaEnMinutos(hora)

        while linea != "" and profesionalDisponible is None:
            profesional = convertirProfesional(linea)

            if profesional[2].lower() == especialidad.lower():
                horarios = profesional[3]

                if dia in horarios and horarios[dia]:
                    minutosInicio = _horaEnMinutos(horarios[dia][0])
                    minutosFin = _horaEnMinutos(horarios[dia][1])
                    duracion = profesional[4]
                    horarioValido = False

                    if (minutosInicio <= minutosHora and
                            minutosHora + duracion <= minutosFin and
                            (minutosHora - minutosInicio) % duracion == 0):
                        horarioValido = True

                    for numero in range(profesional[5]):
                        if minutosHora == minutosFin + numero * duracion:
                            horarioValido = True

                    if horarioValido and not _turnoOcupado(
                            profesional[0], dni, fecha, hora, turnoExcluir):
                        profesionalDisponible = profesional

            linea = archivo.readline()

    except FileNotFoundError:
        print("Todavía no hay profesionales registrados.")
    except (OSError, ValueError) as mensaje:
        print("No se pudo buscar un profesional:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return profesionalDisponible


# Busca el primer turno libre desde hoy, incluyendo los sobreturnos.
# Devuelve (profesional, fecha, hora, esSobreturno) o None.
def buscarPrimerTurnoLibre(especialidad, dni, turnoExcluir=None):
    fechaActual = datetime.now().date()
    fechaHoy = fechaActual
    horaActual = datetime.now().hour * 60 + datetime.now().minute

    while True:
        diaSemana = diasSemana[fechaActual.weekday()]
        fecha = fechaActual.strftime("%d/%m/%Y")
        profesionalDisponible = None
        horaDisponible = None
        sobreTurnoDisponible = False
        mejorHorario = 1440
        archivo = None

        try:
            archivo = open(ARCHIVO_PROFESIONALES, "rt")
            linea = archivo.readline()

            while linea != "":
                profesional = convertirProfesional(linea)

                if profesional[2].lower() == especialidad.lower():
                    horarioDia = profesional[3][diaSemana]

                    if horarioDia:
                        minutosInicio = _horaEnMinutos(horarioDia[0])
                        minutosFin = _horaEnMinutos(horarioDia[1])
                        duracion = profesional[4]

                        # Primero se recorren los horarios habituales.
                        minutos = minutosInicio

                        while minutos + duracion <= minutosFin:
                            hora = (str(minutos // 60).zfill(2) + ":" +
                                    str(minutos % 60).zfill(2))

                            esFuturo = (
                                fechaActual > fechaHoy or minutos > horaActual
                            )

                            esExcluido = (
                                turnoExcluir is not None and
                                turnoExcluir[2] == fecha and
                                turnoExcluir[3] == hora
                            )

                            if (esFuturo and not esExcluido and
                                    minutos < mejorHorario):
                                if not _turnoOcupado(
                                        profesional[0], dni, fecha, hora,
                                        turnoExcluir):
                                    mejorHorario = minutos
                                    profesionalDisponible = profesional
                                    horaDisponible = hora
                                    sobreTurnoDisponible = False

                            minutos += duracion

                        # Luego se consideran los sobreturnos posteriores al cierre.
                        for numero in range(profesional[5]):
                            minutos = minutosFin + numero * duracion

                            if minutos + duracion <= 1440:
                                hora = (str(minutos // 60).zfill(2) + ":" +
                                        str(minutos % 60).zfill(2))

                                esFuturo = (
                                    fechaActual > fechaHoy or minutos > horaActual
                                )

                                esExcluido = (
                                    turnoExcluir is not None and
                                    turnoExcluir[2] == fecha and
                                    turnoExcluir[3] == hora
                                )

                                if (esFuturo and not esExcluido and
                                        minutos < mejorHorario):
                                    if not _turnoOcupado(
                                            profesional[0], dni, fecha, hora,
                                            turnoExcluir):
                                        mejorHorario = minutos
                                        profesionalDisponible = profesional
                                        horaDisponible = hora
                                        sobreTurnoDisponible = True

                linea = archivo.readline()

        except FileNotFoundError:
            print("Todavía no hay profesionales registrados.")
            return None
        except (OSError, ValueError) as mensaje:
            print("No se pudo buscar el primer turno libre:", mensaje)
            return None
        finally:
            if archivo is not None:
                archivo.close()

        if profesionalDisponible is not None:
            return (
                profesionalDisponible, fecha, horaDisponible,
                sobreTurnoDisponible
            )

        fechaActual = fechaActual + timedelta(days=1)


# Busca un profesional para una fecha y hora elegidas manualmente.
def buscarProfesionalParaFechaHora(especialidad, dni, dia, fecha, hora,
                                   turnoExcluir=None):
    if not validarHora(hora):
        return None

    return buscarPrimerProfesionalConTurnoLibre(
        especialidad, dia, fecha, hora, dni, turnoExcluir
    )


# Lista los turnos del día actual sin acumularlos en una lista.
def listarTurnosDelDia():
    fecha = datetime.now().strftime("%d/%m/%Y")
    mostrarProfesionalesDelDia()
    legajo = input("Ingrese el legajo del profesional para listar sus turnos de hoy: ")
    profesional = buscarProfesionalPorLegajo(legajo)

    if profesional is None:
        print("No se encontró un profesional con ese legajo.")
        return

    print("Turnos del día " + fecha + " para " + profesional[1] + ":")
    hayTurnos = False
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt")
        linea = archivo.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")

            if (len(datos) == 4 and datos[1] == legajo and
                    datos[2] == fecha):
                hayTurnos = True
                print("Paciente DNI: " + datos[0] + ", Hora: " + datos[3])

            linea = archivo.readline()

        if not hayTurnos:
            print("No hay turnos programados para hoy.")

    except FileNotFoundError:
        print("Todavía no hay turnos registrados.")
    except OSError as mensaje:
        print("No se pudo leer el archivo de turnos:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()
