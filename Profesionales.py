
import os
from datetime import datetime, timedelta
import Especialidades
import Pacientes


ARCHIVO_PROFESIONALES = "profesionales.txt"
ARCHIVO_TURNOS = "turnos.txt"
ARCHIVO_AUXILIAR = "profesionales_aux.txt"


def cargarProfesionalesIniciales():
    """Crea profesionales de ejemplo solo si todavía no existe el archivo."""
    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        archivo.close()
        return
    except FileNotFoundError:
        pass
    except OSError as mensaje:
        print("No se pudo consultar el archivo de profesionales:", mensaje)
        return

    especialidades = Especialidades.cargarEspecialidades()
    if not especialidades:
        print("No se cargaron profesionales: no hay especialidades disponibles.")
        return

    diasLaborales = obtenerDiasSemana()[:5]
    horarios = {
        dia: [["09:00", "13:00"], ["14:00", "18:00"]]
        if dia in diasLaborales else []
        for dia in obtenerDiasSemana()
    }
    profesionales = [
        ["1", "Ana Ejemplo", especialidades[0], horarios, 30, 2],
        ["2", "Bruno Ejemplo", especialidades[min(1, len(especialidades) - 1)], horarios, 30, 1],
        ["3", "Carla Ejemplo", especialidades[min(2, len(especialidades) - 1)], horarios, 20, 1]
    ]

    archivo = None
    try:
        archivo = open(ARCHIVO_PROFESIONALES, "wt", encoding="utf-8")
        for profesional in profesionales:
            archivo.write(convertirLinea(profesional))
        print("Se cargaron los profesionales iniciales de ejemplo.")
    except OSError as mensaje:
        print("No se pudieron guardar los profesionales iniciales:", mensaje)
    finally:
        if archivo is not None:
            archivo.close()


def obtenerDiasSemana():
    return [
        "lunes", "martes", "miércoles", "jueves",
        "viernes", "sábado", "domingo"
    ]


def validarTexto(texto):
    return texto.strip() != "" and ";" not in texto and "\n" not in texto


# Convierte una línea del archivo en un único profesional.
# Acepta el formato anterior de 19 campos y el nuevo de 33.
# Estructura: [legajo, nombre, especialidad, horarios, duracion, sobreturnos]
def convertirProfesional(linea):
    datos = linea.rstrip("\n").split(";")

    if len(datos) != 19 and len(datos) != 33:
        raise ValueError("El registro del profesional tiene una cantidad incorrecta de campos.")

    horarios = {}
    diasSemana = obtenerDiasSemana()
    posicion = 5

    for dia in diasSemana:
        if len(datos) == 19:
            horaInicio = datos[posicion]
            horaFin = datos[posicion + 1]

            if horaInicio == "-" and horaFin == "-":
                horarios[dia] = []
            elif validarRangoHorario(horaInicio, horaFin):
                horarios[dia] = [[horaInicio, horaFin]]
            else:
                raise ValueError("El horario de un profesional es inválido.")

            posicion += 2

        else:
            horaInicio1 = datos[posicion]
            horaFin1 = datos[posicion + 1]
            horaInicio2 = datos[posicion + 2]
            horaFin2 = datos[posicion + 3]

            intervalos = []

            if horaInicio1 != "-" and horaFin1 != "-":
                if validarRangoHorario(horaInicio1, horaFin1):
                    intervalos.append([horaInicio1, horaFin1])
                else:
                    raise ValueError("El primer intervalo de horario es inválido.")
            elif horaInicio1 != "-" or horaFin1 != "-":
                raise ValueError("El primer intervalo está incompleto.")

            if horaInicio2 != "-" and horaFin2 != "-":
                if validarRangoHorario(horaInicio2, horaFin2):
                    if intervalos:
                        if _horaEnMinutos(horaInicio2) < _horaEnMinutos(horaFin1):
                            raise ValueError("Los intervalos de horario se superponen o están desordenados.")

                    intervalos.append([horaInicio2, horaFin2])
                else:
                    raise ValueError("El segundo intervalo de horario es inválido.")
            elif horaInicio2 != "-" or horaFin2 != "-":
                raise ValueError("El segundo intervalo está incompleto.")

            horarios[dia] = intervalos
            posicion += 4

    return [
        datos[0], datos[1], datos[2], horarios,
        int(datos[3]), int(datos[4])
    ]


# Convierte un profesional en una línea para guardarlo en el archivo.
# El nuevo formato utiliza 33 campos.
def convertirLinea(profesional):
    datos = [
        profesional[0],
        profesional[1],
        profesional[2],
        str(profesional[4]),
        str(profesional[5])
    ]

    horarios = profesional[3]
    diasSemana = obtenerDiasSemana()

    for dia in diasSemana:
        intervalos = horarios[dia]

        if len(intervalos) >= 1:
            datos.append(intervalos[0][0])
            datos.append(intervalos[0][1])
        else:
            datos.append("-")
            datos.append("-")

        if len(intervalos) >= 2:
            datos.append(intervalos[1][0])
            datos.append(intervalos[1][1])
        else:
            datos.append("-")
            datos.append("-")

    return ";".join(datos) + "\n"


# Busca recursivamente un profesional leyendo el archivo.
def _buscarProfesionalRecursivo(archivo, legajo):
    linea = archivo.readline()

    if linea == "":
        return None

    profesional = convertirProfesional(linea)

    if profesional[0] == str(legajo):
        return profesional

    return _buscarProfesionalRecursivo(archivo, legajo)


# Busca un profesional por legajo.
def buscarProfesionalPorLegajo(legajo):
    profesionalEncontrado = None
    archivo = None

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        profesionalEncontrado = _buscarProfesionalRecursivo(archivo, legajo)

    except FileNotFoundError:
        print("Todavía no existe el archivo de profesionales.")
    except (OSError, ValueError, RecursionError) as mensaje:
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
        archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        linea = archivo.readline()

        while linea != "" and not existe:
            profesional = convertirProfesional(linea)

            if profesional[2].lower() == especialidad.lower():
                existe = True

            linea = archivo.readline()

    except FileNotFoundError:
        existe = False
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
        minutosInicio = _horaEnMinutos(horaInicio)
        minutosFin = _horaEnMinutos(horaFin)

        if minutosInicio < minutosFin:
            rangoValido = True

    return rangoValido


# Convierte HH:MM a minutos desde la medianoche.
def _horaEnMinutos(hora):
    partes = hora.split(":")
    return int(partes[0]) * 60 + int(partes[1])


# Solicita los intervalos de atención de un día.
# Devuelve None si el usuario cancela, [] si no atiende.
def pedirHorarioDia(dia):
    print("\nConfiguración del " + dia)
    print("Ingrese 0 si desea cancelar la carga de horarios.")

    atiende = input("¿El profesional atiende ese día? Ingrese s o n: ").lower()

    while atiende not in ["s", "n", "0"]:
        print("Opción incorrecta.")
        atiende = input("Ingrese s, n o 0 para cancelar: ").lower()

    if atiende == "0":
        return None

    if atiende == "n":
        return []

    horaInicio = input("Ingrese el comienzo del primer horario (HH:MM): ")
    horaFin = input("Ingrese el fin del primer horario (HH:MM): ")

    while not validarRangoHorario(horaInicio, horaFin):
        print("Horario inválido.")
        horaInicio = input("Ingrese nuevamente la hora de inicio: ")
        horaFin = input("Ingrese nuevamente la hora de fin: ")

    intervalos = [[horaInicio, horaFin]]

    segundoHorario = input("¿Tiene un segundo horario de atención? (s/n): ").lower()

    while segundoHorario not in ["s", "n"]:
        print("Opción incorrecta.")
        segundoHorario = input("Ingrese s o n: ").lower()

    if segundoHorario == "s":
        horaInicio2 = input("Ingrese el comienzo del segundo horario (HH:MM): ")
        horaFin2 = input("Ingrese el fin del segundo horario (HH:MM): ")

        while (not validarRangoHorario(horaInicio2, horaFin2)
               or _horaEnMinutos(horaInicio2) < _horaEnMinutos(horaFin)):
            print("El segundo horario debe ser válido y comenzar cuando termine el primero.")
            horaInicio2 = input("Ingrese nuevamente la hora de inicio: ")
            horaFin2 = input("Ingrese nuevamente la hora de fin: ")

        intervalos.append([horaInicio2, horaFin2])

    return intervalos


# Devuelve el horario de un profesional para un día concreto.
def getHorarioProfesional(legajo, dia):
    horario = None
    profesional = buscarProfesionalPorLegajo(legajo)

    if profesional is not None and dia in profesional[3]:
        intervalos = profesional[3][dia]

        if intervalos:
            horario = ""

            for posicion in range(len(intervalos)):
                if posicion > 0:
                    horario += " y "

                horario += (
                    intervalos[posicion][0] + " a " +
                    intervalos[posicion][1] + " hs"
                )
        else:
            horario = "No atiende"

    return horario


# Comprueba si un profesional tiene turnos asignados.
def tieneTurnos(legajo):
    tieneTurnosAsignados = False
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt", encoding="utf-8")
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


# Muestra los intervalos de atención de un profesional.
def mostrarHorarios(horarios):
    diasSemana = obtenerDiasSemana()

    for dia in diasSemana:
        if horarios[dia]:
            print(dia + ": ", end="")

            for posicion in range(len(horarios[dia])):
                if posicion > 0:
                    print(" y ", end="")

                print(
                    horarios[dia][posicion][0] + " a " +
                    horarios[dia][posicion][1] + " hs",
                    end=""
                )

            print()
        else:
            print(dia + ": No atiende")


# Muestra los profesionales leyendo el archivo registro por registro.
def mostrarProfesionales():
    archivo = None
    hayProfesionales = False

    print("Los profesionales disponibles son:")

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        linea = archivo.readline()

        while linea != "":
            profesional = convertirProfesional(linea)
            hayProfesionales = True

            print("Legajo: " + profesional[0])
            print("Nombre: " + profesional[1])
            print("Especialidad: " + profesional[2])
            print("Duración de cada turno: " + str(profesional[4]) + " minutos")
            print("Cantidad de sobreturnos: " + str(profesional[5]))
            print("Horarios:")
            mostrarHorarios(profesional[3])
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
    diasSemana = obtenerDiasSemana()
    diaActual = diasSemana[datetime.now().weekday()]
    hayProfesionales = False

    print("Los profesionales que atienden hoy (" + diaActual + ") son:")

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
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
                print("Horarios:")
                print(getHorarioProfesional(profesional[0], diaActual))
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
        mostrarHorarios(profesionalEncontrado[3])


# Reescribe el archivo auxiliarmente para modificar o eliminar un registro.
def _reescribirProfesionales(legajo, profesionalNuevo=None):
    archivoOriginal = None
    archivoAuxiliar = None
    encontrado = False
    operacionCorrecta = False

    try:
        archivoOriginal = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        archivoAuxiliar = open(ARCHIVO_AUXILIAR, "wt", encoding="utf-8")

        linea = archivoOriginal.readline()

        while linea != "":
            profesional = convertirProfesional(linea)

            if profesional[0] == str(legajo) and not encontrado:
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
def actualizarEspecialidadProfesionales(nombreActual, nombreNuevo):
    archivoOriginal = None
    archivoAuxiliar = None
    correcto = False

    try:
        archivoOriginal = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        archivoAuxiliar = open(ARCHIVO_AUXILIAR, "wt", encoding="utf-8")

        linea = archivoOriginal.readline()

        while linea != "":
            profesional = convertirProfesional(linea)

            if profesional[2].lower() == nombreActual.lower():
                profesional[2] = nombreNuevo
                archivoAuxiliar.write(convertirLinea(profesional))
            else:
                archivoAuxiliar.write(linea)

            linea = archivoOriginal.readline()

        archivoOriginal.close()
        archivoOriginal = None
        archivoAuxiliar.close()
        archivoAuxiliar = None

        os.remove(ARCHIVO_PROFESIONALES)
        os.rename(ARCHIVO_AUXILIAR, ARCHIVO_PROFESIONALES)
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

    while eleccion != 7:
        eleccion = input(
            "Gestión de profesionales, ingrese:\n"
            "1 para agregar un profesional.\n"
            "2 para quitar un profesional.\n"
            "3 para modificar un profesional.\n"
            "4 para modificar el horario de un profesional.\n"
            "5 para buscar un profesional por legajo.\n"
            "6 para listar todos los profesionales.\n"
            "7 para salir al menú principal.\n"
        )

        while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > 7:
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 7: ")

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
                mostrarProfesionales()
            case 7:
                print("Volvemos al menú principal.")


# Modifica el horario de un día y guarda el profesional en el archivo.
def modificarHorario():
    legajo = input("Ingrese el legajo del profesional: ")
    profesionalEncontrado = buscarProfesionalPorLegajo(legajo)

    if profesionalEncontrado is None:
        print("No se encontró un profesional con el legajo ingresado.")
        return

    horarios = profesionalEncontrado[3]
    diasSemana = obtenerDiasSemana()

    print("Días disponibles:")

    for dia in diasSemana:
        print(dia)

    dia = input("Ingrese el día que desea modificar: ").lower()

    while dia not in horarios:
        print("Día incorrecto.")
        dia = input("Ingrese nuevamente el día: ").lower()

    print("Horario actual: " + getHorarioProfesional(legajo, dia))
    print("Ingrese 0 si desea cancelar la modificación.")

    nuevoHorario = pedirHorarioDia(dia)

    if nuevoHorario is None:
        print("Modificación cancelada.")
    else:
        horarios[dia] = nuevoHorario

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
    nombre = input("Ingrese nuevo nombre o presione enter para mantenerlo: ").strip()

    while nombre != "" and not validarTexto(nombre):
        print("El nombre no puede estar vacío ni contener punto y coma.")
        nombre = input("Ingrese nuevamente el nombre: ").strip()

    if nombre == "":
        nombre = profesionalEncontrado[1]

    print("Especialidad actual: " + profesionalEncontrado[2])
    Especialidades.listarEspecialidades(especialidades)

    especialidad = input(
        "Ingrese nueva especialidad o presione enter para mantener la actual: "
    ).strip()

    if especialidad == "":
        especialidad = profesionalEncontrado[2]
    else:
        while not Especialidades.especialidadRegistrada(
                especialidades, especialidad):
            print("La especialidad ingresada no está registrada.")
            especialidad = input("Ingrese de nuevo la especialidad: ").strip()

        posicion = Especialidades.buscarPosicionEspecialidad(
            especialidades, especialidad
        )

        especialidad = especialidades[posicion]

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


def obtenerProximoLegajo():
    """Devuelve el mayor legajo numérico existente más uno."""
    mayorLegajo = 0
    archivo = None

    try:
        archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        linea = archivo.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")
            if len(datos) in [19, 33] and datos[0].isdigit():
                mayorLegajo = max(mayorLegajo, int(datos[0]))
            linea = archivo.readline()

    except FileNotFoundError:
        pass
    except OSError as mensaje:
        print("No se pudo determinar el próximo legajo:", mensaje)
        return None
    finally:
        if archivo is not None:
            archivo.close()

    return str(mayorLegajo + 1)


# Registra un profesional nuevo con legajo numérico consecutivo.
def agregarProfesionales():
    especialidades = Especialidades.cargarEspecialidades()

    if not especialidades:
        print("No se pueden añadir profesionales porque no hay especialidades registradas.")
        return

    legajo = obtenerProximoLegajo()
    if legajo is None:
        return
    print("Legajo asignado:", legajo)

    nombre = input("Ingrese nombre del profesional: ").strip()

    while not validarTexto(nombre):
        print("El nombre no puede estar vacío ni contener punto y coma.")
        nombre = input("Ingrese nuevamente el nombre: ").strip()

    Especialidades.listarEspecialidades(especialidades)
    especialidad = input("Ingrese especialidad del profesional: ").strip()

    while not Especialidades.especialidadRegistrada(especialidades, especialidad):
        print("La especialidad ingresada no está registrada.")
        especialidad = input("Ingrese de nuevo la especialidad: ").strip()

    posicion = Especialidades.buscarPosicionEspecialidad(
        especialidades, especialidad
    )
    especialidad = especialidades[posicion]

    duracionTurno = input("Ingrese la duración de cada turno en minutos: ")

    while not duracionTurno.isdigit() or int(duracionTurno) <= 0:
        print("La duración debe ser un número mayor que cero.")
        duracionTurno = input("Ingrese nuevamente la duración en minutos: ")

    duracionTurno = int(duracionTurno)
    horarios = {}
    diasSemana = obtenerDiasSemana()

    for dia in diasSemana:
        nuevoHorario = pedirHorarioDia(dia)

        if nuevoHorario is None:
            print("Carga del profesional cancelada.")
            return

        horarios[dia] = nuevoHorario

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
        archivo = open(ARCHIVO_PROFESIONALES, "at", encoding="utf-8")
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


# Comprueba si una fecha/hora está ocupada por el profesional o por el paciente.
# turnoExcluir se utiliza al reprogramar un turno.
def _turnoOcupado(legajo, dni, fecha, hora, turnoExcluir=None):
    ocupado = False
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt", encoding="utf-8")
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
                    if datos[1] == str(legajo) or datos[0] == str(dni):
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
        archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
        linea = archivo.readline()
        minutosHora = _horaEnMinutos(hora)

        while linea != "" and profesionalDisponible is None:
            profesional = convertirProfesional(linea)

            if profesional[2].lower() == especialidad.lower():
                intervalos = profesional[3][dia]
                duracion = profesional[4]
                horarioValido = False

                for intervalo in intervalos:
                    minutosInicio = _horaEnMinutos(intervalo[0])
                    minutosFin = _horaEnMinutos(intervalo[1])

                    if (minutosInicio <= minutosHora and
                            minutosHora + duracion <= minutosFin and
                            (minutosHora - minutosInicio) % duracion == 0):
                        horarioValido = True

                if intervalos:
                    minutosFin = _horaEnMinutos(intervalos[-1][1])

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
# La búsqueda se limita a los próximos 365 días.
# Devuelve (profesional, fecha, hora, esSobreturno) o None.
def buscarPrimerTurnoLibre(especialidad, dni, turnoExcluir=None):
    fechaActual = datetime.now().date()
    fechaHoy = fechaActual
    horaActual = datetime.now().hour * 60 + datetime.now().minute
    diasBuscados = 0
    resultado = None

    while diasBuscados < 365 and resultado is None:
        diasSemana = obtenerDiasSemana()
        diaSemana = diasSemana[fechaActual.weekday()]
        fecha = fechaActual.strftime("%d/%m/%Y")

        profesionalDisponible = None
        horaDisponible = None
        sobreTurnoDisponible = False
        mejorHorario = 1440
        archivo = None

        try:
            archivo = open(ARCHIVO_PROFESIONALES, "rt", encoding="utf-8")
            linea = archivo.readline()

            while linea != "":
                profesional = convertirProfesional(linea)

                if profesional[2].lower() == especialidad.lower():
                    intervalos = profesional[3][diaSemana]
                    duracion = profesional[4]

                    for intervalo in intervalos:
                        minutosInicio = _horaEnMinutos(intervalo[0])
                        minutosFin = _horaEnMinutos(intervalo[1])
                        minutos = minutosInicio

                        while minutos + duracion <= minutosFin:
                            hora = (
                                str(minutos // 60).zfill(2) + ":" +
                                str(minutos % 60).zfill(2)
                            )

                            esFuturo = (
                                fechaActual > fechaHoy or minutos > horaActual
                            )

                            if esFuturo and minutos < mejorHorario:
                                if not _turnoOcupado(
                                        profesional[0], dni, fecha, hora,
                                        turnoExcluir):
                                    mejorHorario = minutos
                                    profesionalDisponible = profesional
                                    horaDisponible = hora
                                    sobreTurnoDisponible = False

                            minutos += duracion

                    if intervalos:
                        minutosFin = _horaEnMinutos(intervalos[-1][1])

                        for numero in range(profesional[5]):
                            minutos = minutosFin + numero * duracion

                            if minutos + duracion <= 1440:
                                hora = (
                                    str(minutos // 60).zfill(2) + ":" +
                                    str(minutos % 60).zfill(2)
                                )

                                esFuturo = (
                                    fechaActual > fechaHoy or minutos > horaActual
                                )

                                if esFuturo and minutos < mejorHorario:
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
            resultado = (
                profesionalDisponible, fecha, horaDisponible,
                sobreTurnoDisponible
            )
        else:
            fechaActual = fechaActual + timedelta(days=1)
            diasBuscados += 1

    if resultado is None:
        print("No se encontraron turnos disponibles dentro de los próximos 365 días.")

    return resultado


# Busca un profesional para una fecha y hora elegidas manualmente.
def buscarProfesionalParaFechaHora(especialidad, dni, dia, fecha, hora,
                                   turnoExcluir=None):
    if not validarHora(hora):
        return None

    return buscarPrimerProfesionalConTurnoLibre(
        especialidad, dia, fecha, hora, dni, turnoExcluir
    )


# Lista los turnos del día actual de un profesional.
def listarTurnosDelDia():
    fecha = datetime.now().strftime("%d/%m/%Y")
    mostrarProfesionalesDelDia()

    legajo = input(
        "Ingrese el legajo del profesional para listar sus turnos de hoy: "
    )

    profesional = buscarProfesionalPorLegajo(legajo)

    if profesional is None:
        print("No se encontró un profesional con ese legajo.")
        return

    print("Turnos del día " + fecha + " para " + profesional[1] + ":")
    hayTurnos = False
    archivo = None

    try:
        archivo = open(ARCHIVO_TURNOS, "rt", encoding="utf-8")
        linea = archivo.readline()

        while linea != "":
            datos = linea.rstrip("\n").split(";")

            if (len(datos) == 4 and datos[1] == legajo and
                    datos[2] == fecha):
                hayTurnos = True
                paciente = Pacientes.buscarPacientePorDNI(datos[0])
                if paciente is None:
                    nombrePaciente = "DNI " + datos[0]
                else:
                    nombrePaciente = (
                        paciente["nombre"] + " " + paciente["apellido"] +
                        " (DNI " + datos[0] + ")"
                    )
                print("Paciente: " + nombrePaciente + ", Hora: " + datos[3])

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

