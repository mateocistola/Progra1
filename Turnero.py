import datetime
import Calendario_de_Turnos

profesionales = [
    ["1", "Perez, Carolina", "Cardiologia"],
    ["2", "Gomez, Alejandra", "Clinica Medica"],
    ["3", "Lopez, Eduardo", "Traumatologia"]
]

turnos = []


# Para saber qué médicos están disponibles
def mostrarProfesionales():
    """print("Los profesionales disponibles son: ")
    for p in profesionales:
        print("ID: " + p[0] + "\n Nombre: " + p[1] + "\n Especialidad: " + p[2])"""
    
    print('-----------------------------------')
    print('|     Sacar Turno con          |')
    print('| CARDIOLOGO ..........|1|')
    print('| CLINICA MEDICA ....|2|')
    print('| TRAUMATOLOGO ...|3|')


def darTurno():
    mostrarProfesionales()

    idProfesional = input("Ingrese el Profecional re-querido : ")

    dni = input("Ingrese DNI del paciente")
    while not (len(dni) == 7 or len(dni) == 8) or not dni.isdigit():
        print("DNI no valido")
        dni = input("Ingrese nuevamente el DNI del paciente : ")

    while True:
        try:
            Calendario_de_Turnos.mostrar_meses()
            fecha = datetime.datetime.strptime(input("Ingrese la fecha xx/xx/xxxx"), "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha incorrecta, ingrese la fecha de nuevo")

    while True:
        try:
            hora = datetime.datetime.strptime(input("Ingrese la hora H:M"), "%H:%M").time()
            break
        except ValueError:
            print("Hora incorrecta, ingrese la hora de nuevo")
    for p in profesionales:  # chequeo si existe el id del profesional ingresado en la lista de profesionales
        if (p[0] == idProfesional):
            turnos.append([dni, idProfesional, fecha,
                           hora])  # por ahora la lista de turnos es global para todos los profesionales #Metería el idProfesional aquí también
            print(
                "Turno dado correctamente")  # faltaria chequear antes de dar un turno si no existia un turno ya en ese horario
            return
    print("no se encontró un profesional con id de especialidad ingresada")


def reprogramarTurno():
    dni = input("Ingrese DNI del paciente")
    while not (len(dni) == 7 or len(dni) == 8) or not dni.isdigit():
        print("DNI no valido")
        dni = input("Ingrese nuevamente el DNI del paciente")
    while True:
        try:
            fecha = datetime.datetime.strptime(input("Ingrese la fecha"), "%d/%m/%Y")
            break
        except ValueError:
            print("Fecha incorrecta, ingrese la fecha de nuevo")
    while True:
        try:
            hora = datetime.datetime.strptime(input("Ingrese nueva hora"), "%H:%M").time()
            break
        except ValueError:
            print("Hora incorrecta, ingrese la hora de nuevo")

    for t in turnos:
        if (t[0] == dni):
            t[2] = fecha
            t[3] = hora
            print(
                "Turno reprogramado")  # aca falta chequear tambien si el nuevo horario ya estaba ocupado para no pisar turnos
            return  # salir del bucle y no seguir buscando
    print("No se encontró un turno para el DNI del paciente ingresado")


def cancelarTurno():
    dni = input("Ingrese DNI del paciente")
    while not (len(dni) == 7 or len(dni) == 8) or not dni.isdigit():
        print("DNI no valido")
        dni = input("Ingrese nuevamente el DNI del paciente")
    for t in turnos:
        if (t[0] == dni):
            turnos.remove(t)
            print("Turno cancelado")
            return  # sale del bucle y no sigue buscando al pedo
    print("No se encontró un turno para el paciente ingresado")


def listarTurnos():
    for t in turnos:
        print("Paciente DNI: " + t[0] + "Profesional ID: " + t[1] + "Fecha: " + t[2].strftime("%d/%m/%Y") + " Hora: " + t[3].strftime("%H:%M"))
