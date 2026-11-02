from datetime import datetime
import os

import Especialidades
import Profesionales
import Pacientes


ARCHIVO_TURNOS = "turnos.txt"
ARCHIVO_TURNOS_AUXILIAR = "turnos_aux.txt"


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
        if (partes[0].isdigit() and partes[1].isdigit()
                and partes[2].isdigit()):
            dia = int(partes[0])
            mes = int(partes[1])
            año = int(partes[2])

            cantidadDias = obtenercantdias(mes, año)

            if 1 <= dia <= cantidadDias:
                fechaValida = True

    return fechaValida


# Comprueba que la fecha y hora sean posteriores al momento actual.
def validarFechaHoraFutura(fecha, hora):
    partesFecha = fecha.split("/")
    partesHora = hora.split(":")

    dia = int(partesFecha[0])
    mes = int(partesFecha[1])
    año = int(partesFecha[2])
    horas = int(partesHora[0])
    minutos = int(partesHora[1])

    fechaHoraTurno = datetime(año, mes, dia, horas, minutos)
    fechaHoraActual = datetime.now()

    return fechaHoraTurno > fechaHoraActual


# Solicita fecha y hora hasta que sean válidas y futuras.
def ingresarFechaHora():
    fechaHoraValida = False
    fecha = ""
    hora = ""

    while not fechaHoraValida:
        fecha = input("Ingrese la fecha con formato día/mes/año: ")

        while not validarFecha(fecha):
            print("Fecha incorrecta.")
            fecha = input("Ingrese de nuevo la fecha: ")

        hora = input("Ingrese la hora con formato HH:MM: ")

        while not validarHora(hora):
            print("Hora incorrecta.")
            hora = input("Ingrese nuevamente la hora: ")

        if validarFechaHoraFutura(fecha, hora):
            fechaHoraValida = True
        else:
            print("No se puede asignar un turno en una fecha u hora pasada.")

    return fecha, hora


def obtenerDiaSemana(fecha):
    partesFecha = fecha.split("/")
    dia = int(partesFecha[0])
    mes = int(partesFecha[1])
    año = int(partesFecha[2])

    fechaTurno = datetime(año, mes, dia)
    dias = [
        "lunes", "martes", "miércoles", "jueves",
        "viernes", "sábado", "domingo"
    ]

    return dias[fechaTurno.weekday()]


# Lee turnos.txt de a una línea para saber si hay registros.
def hayTurnosRegistrados():
    hayTurnos = False
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt")
        linea = archivo.readline()

        if linea != "":
            hayTurnos = True

    except FileNotFoundError:
        hayTurnos = False
    except OSError as mensaje:
        print("No se pudo consultar el archivo de turnos:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return hayTurnos


# Agrega un turno al final del archivo.
def guardarTurno(turno):
    archivo = None
    guardado = False

    try:
        archivo = open(ARCHIVO_TURNOS, "at")
        archivo.write(
            turno[0] + ";" + turno[1] + ";" +
            turno[2] + ";" + turno[3] + "\n"
        )
        guardado = True
    except OSError as mensaje:
        print("No se pudo guardar el turno:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return guardado


# Reescribe turnos.txt para reemplazar o eliminar un turno exacto.
# Si turnoNuevo es None, elimina el registro seleccionado.
def actualizarTurno(turnoOriginal, turnoNuevo=None):
    archivoOriginal = None
    archivoAuxiliar = None
    encontrado = False
    actualizacionCorrecta = False

    try:
        archivoOriginal = open(ARCHIVO_TURNOS, "rt")
        archivoAuxiliar = open(ARCHIVO_TURNOS_AUXILIAR, "wt")

        linea = archivoOriginal.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")

            if (len(datos) == 4 and
                    datos[0] == turnoOriginal[0] and
                    datos[1] == turnoOriginal[1] and
                    datos[2] == turnoOriginal[2] and
                    datos[3] == turnoOriginal[3] and
                    not encontrado):

                encontrado = True

                if turnoNuevo is not None:
                    archivoAuxiliar.write(
                        turnoNuevo[0] + ";" + turnoNuevo[1] + ";" +
                        turnoNuevo[2] + ";" + turnoNuevo[3] + "\n"
                    )
            else:
                archivoAuxiliar.write(linea)

            linea = archivoOriginal.readline()

        archivoOriginal.close()
        archivoOriginal = None
        archivoAuxiliar.close()
        archivoAuxiliar = None

        if encontrado:
            os.remove(ARCHIVO_TURNOS)
            os.rename(ARCHIVO_TURNOS_AUXILIAR, ARCHIVO_TURNOS)
            actualizacionCorrecta = True
        else:
            os.remove(ARCHIVO_TURNOS_AUXILIAR)
            print("No se encontró el turno que se quería actualizar.")

    except FileNotFoundError:
        print("Todavía no hay turnos registrados.")
    except OSError as mensaje:
        print("No se pudo actualizar el archivo de turnos:", mensaje)
    finally:
        if archivoOriginal is not None:
            archivoOriginal.close()
        if archivoAuxiliar is not None:
            archivoAuxiliar.close()

    return actualizacionCorrecta


# Lee los turnos de un paciente. Solo conserva en memoria los registros
# de ese DNI porque se necesitan para que el usuario elija uno.
def obtenerTurnosDePaciente(dniPaciente):
    turnosPaciente = []
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt")
        linea = archivo.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")

            if len(datos) == 4 and datos[0] == dniPaciente:
                turnosPaciente.append(datos)

            linea = archivo.readline()

    except FileNotFoundError:
        pass
    except OSError as mensaje:
        print("No se pudieron leer los turnos:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()

    return turnosPaciente


# Da un turno al paciente. Profesionales y turnos se consultan desde archivos.
def darTurno():
    especialidades = Especialidades.cargarEspecialidades()
    if not especialidades:
        print("No hay especialidades registradas.")
        return

    Especialidades.listarEspecialidades(especialidades)
    opcion = input("Seleccione el número de la especialidad: ")

    while (not opcion.isdigit() or int(opcion) < 1
           or int(opcion) > len(especialidades)):
        print("Opción incorrecta.")
        opcion = input("Seleccione nuevamente la especialidad: ")

    especialidad = especialidades[int(opcion) - 1]

    if not Profesionales.existeProfesionalPorEspecialidad(especialidad):
        print("No hay profesionales registrados para esa especialidad.")
        return

    dni = input("Ingrese el DNI del paciente: ")
    pacienteEncontrado = Pacientes.buscarPacientePorDNI(dni)

    while pacienteEncontrado is None:
        print("No existe un paciente registrado con ese DNI, ¿querés registrarlo? (S/N)")
        opcion = input("Ingrese su elección: ")

        if opcion.upper() == "S":
            Pacientes.registrarPaciente()

        dni = input("Ingrese nuevamente el DNI del paciente: ")
        pacienteEncontrado = Pacientes.buscarPacientePorDNI(dni)

    resultado = Profesionales.buscarPrimerTurnoLibre(especialidad, dni)

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
        print("No se encontraron turnos disponibles automáticamente.")
        opcion = "N"

    if opcion.upper() != "S":
        turnoValido = False

        while not turnoValido:
            fecha, hora = ingresarFechaHora()
            diaSemana = obtenerDiaSemana(fecha)

            profesionalEncontrado = Profesionales.buscarProfesionalParaFechaHora(
                especialidad, dni, diaSemana, fecha, hora
            )

            if profesionalEncontrado is None:
                print("No hay profesionales disponibles para esa fecha y hora.")
            else:
                turnoValido = True
                horarioDia = profesionalEncontrado[3][diaSemana]
                minutosHora = int(hora[:2]) * 60 + int(hora[3:])
                minutosFin = int(horarioDia[1][:2]) * 60 + int(horarioDia[1][3:])
                esSobreturno = minutosHora >= minutosFin

    turnoNuevo = [dni, profesionalEncontrado[0], fecha, hora]

    if guardarTurno(turnoNuevo):
        print("\nTurno dado correctamente.")
        print("Paciente:", pacienteEncontrado["nombre"], pacienteEncontrado["apellido"])
        print("Profesional:", profesionalEncontrado[1])
        print("Especialidad:", profesionalEncontrado[2])
        print("Fecha:", fecha)
        print("Hora:", hora)

        if esSobreturno:
            print("Turno asignado como sobreturno.")


# Reprograma un turno manteniendo o cambiando la especialidad.
def reprogramarTurno():
    especialidades = Especialidades.cargarEspecialidades()
    dniPaciente = input("Ingrese el DNI del paciente: ")
    paciente = Pacientes.buscarPacientePorDNI(dniPaciente)

    if paciente is None:
        print("No existe un paciente registrado con ese DNI.")
        return

    turnosPaciente = obtenerTurnosDePaciente(dniPaciente)

    if not turnosPaciente:
        print("No hay turnos asignados para el DNI: " + dniPaciente)
        return

    print("Estos son los turnos del paciente:\n")

    for posicion in range(len(turnosPaciente)):
        print("Turno", posicion + 1)
        print("Legajo del profesional: " + turnosPaciente[posicion][1])
        print("Fecha: " + turnosPaciente[posicion][2])
        print("Hora: " + turnosPaciente[posicion][3])
        print()

    opcion = input("Ingrese el número del turno que desea reprogramar: ")

    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(turnosPaciente):
        print("Opción incorrecta.")
        opcion = input("Seleccione nuevamente el turno: ")

    turnoOriginal = turnosPaciente[int(opcion) - 1]

    profesionalActual = Profesionales.buscarProfesionalPorLegajo(
        turnoOriginal[1]
    )

    if profesionalActual is None:
        print("No se encontró el profesional del turno seleccionado.")
        return

    especialidadActual = profesionalActual[2]

    print("\nSeleccione cómo desea buscar el nuevo turno:")
    print("1. Buscar el primer turno disponible de la misma especialidad (" + especialidadActual + ")")
    print("2. Elegir manualmente fecha y hora de la misma especialidad")
    print("3. Cambiar de especialidad y buscar disponibilidad")
    print("4. Volver")

    opcion = input("Ingrese una opción: ")

    while opcion not in ["1", "2", "3", "4"]:
        print("Opción incorrecta.")
        opcion = input("Ingrese una opción entre 1 y 4: ")

    if opcion == "4":
        return

    especialidadElegida = especialidadActual

    if opcion == "3":
        if not especialidades:
            print("No hay especialidades registradas.")
            return

        Especialidades.listarEspecialidades(especialidades)
        seleccion = input("Seleccione el número de la nueva especialidad: ")

        while (not seleccion.isdigit() or int(seleccion) < 1
               or int(seleccion) > len(especialidades)):
            print("Opción incorrecta.")
            seleccion = input("Seleccione nuevamente la especialidad: ")

        especialidadElegida = especialidades[int(seleccion) - 1]

    if not Profesionales.existeProfesionalPorEspecialidad(especialidadElegida):
        print("No hay profesionales registrados para esa especialidad.")
        return

    if opcion in ["1", "3"]:
        resultado = Profesionales.buscarPrimerTurnoLibre(
            especialidadElegida, dniPaciente, turnoOriginal
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
                turnoNuevo = [
                    dniPaciente, profesionalNuevo[0], fechaNueva, horaNueva
                ]

                if actualizarTurno(turnoOriginal, turnoNuevo):
                    print("Turno reprogramado correctamente.")
                return
        else:
            print("No se encontraron turnos disponibles automáticamente.")

        opcionManual = input("¿Desea elegir manualmente una fecha y hora? (S/N): ")

        if opcionManual.upper() != "S":
            print("El turno original se mantiene sin cambios.")
            return

    nuevoTurnoValido = False

    while not nuevoTurnoValido:
        fechaNueva, horaNueva = ingresarFechaHora()
        diaSemana = obtenerDiaSemana(fechaNueva)

        profesionalNuevo = Profesionales.buscarProfesionalParaFechaHora(
            especialidadElegida, dniPaciente, diaSemana, fechaNueva,
            horaNueva, turnoOriginal
        )

        if profesionalNuevo is None:
            print("No hay profesionales disponibles para esa fecha y hora.")
        else:
            turnoNuevo = [
                dniPaciente, profesionalNuevo[0], fechaNueva, horaNueva
            ]

            if actualizarTurno(turnoOriginal, turnoNuevo):
                nuevoTurnoValido = True
                print("\nTurno reprogramado correctamente.")
                print("Profesional:", profesionalNuevo[1])
                print("Especialidad:", profesionalNuevo[2])
                print("Fecha:", fechaNueva)
                print("Hora:", horaNueva)

                horarioDia = profesionalNuevo[3][diaSemana]
                minutosHora = int(horaNueva[:2]) * 60 + int(horaNueva[3:])
                minutosFin = int(horarioDia[1][:2]) * 60 + int(horarioDia[1][3:])

                if minutosHora >= minutosFin:
                    print("Turno asignado como sobreturno.")


# Cancela uno de los turnos de un paciente.
def cancelarTurno():
    dniPaciente = input("Ingrese el DNI del paciente: ")
    turnosPaciente = obtenerTurnosDePaciente(dniPaciente)

    if not turnosPaciente:
        print("No hay turnos registrados para el DNI: " + dniPaciente)
        return

    print("Estos son los turnos del paciente con DNI: " + dniPaciente + "\n")

    for posicion in range(len(turnosPaciente)):
        print("Turno", posicion + 1)
        print("Legajo del profesional: " + turnosPaciente[posicion][1])
        print("Fecha: " + turnosPaciente[posicion][2])
        print("Hora: " + turnosPaciente[posicion][3])
        print()

    opcion = input("Ingrese el número del turno que desea cancelar: ")

    while not opcion.isdigit() or int(opcion) < 1 or int(opcion) > len(turnosPaciente):
        print("Opción incorrecta.")
        opcion = input("Seleccione nuevamente el turno: ")

    turnoCancelar = turnosPaciente[int(opcion) - 1]

    if actualizarTurno(turnoCancelar):
        print("Turno cancelado correctamente.")


# Muestra todos los turnos leyendo el archivo secuencialmente.
def listarTodosLosTurnos():
    archivo = None
    hayTurnos = False

    try:
        archivo = open(ARCHIVO_TURNOS, "rt")
        linea = archivo.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")

            if len(datos) == 4:
                hayTurnos = True
                print("DNI del paciente: " + datos[0])
                print("Legajo del profesional: " + datos[1])
                print("Fecha: " + datos[2])
                print("Hora: " + datos[3])
                print()

            linea = archivo.readline()

        if not hayTurnos:
            print("No hay turnos registrados en el sistema.")

    except FileNotFoundError:
        print("No hay turnos registrados en el sistema.")
    except OSError as mensaje:
        print("No se pudo leer el archivo de turnos:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()


# Lista los turnos de un paciente sin cargar los turnos de otros pacientes.
def listarTurnosDePaciente():
    dniPaciente = input("Ingrese el DNI del paciente: ")
    paciente = Pacientes.buscarPacientePorDNI(dniPaciente)

    if paciente is None:
        print("No existe un paciente registrado con ese DNI.")
        return

    turnosPaciente = obtenerTurnosDePaciente(dniPaciente)

    if not turnosPaciente:
        print("No hay turnos registrados para el paciente con DNI: " + dniPaciente)
    else:
        print("Estos son los turnos del paciente con DNI: " + dniPaciente + "\n")

        for posicion in range(len(turnosPaciente)):
            print("Turno", posicion + 1)
            print("Legajo del profesional: " + turnosPaciente[posicion][1])
            print("Fecha: " + turnosPaciente[posicion][2])
            print("Hora: " + turnosPaciente[posicion][3])
            print()
