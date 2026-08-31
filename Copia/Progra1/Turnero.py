profesionales = [
    ["1", "Perez, Carolina", "Cardiologia"],
    ["2", "Gomez, Alejandra", "Clinica Medica"],
    ["3", "Lopez, Eduardo", "Traumatologia"]
]

turnos = [

]
#Para saber qué médicos están disponibles
def mostrarProfesionales():
    print("Los profesionales disponibles son: ")
    for p in profesionales:
        print("ID: " + p[0] + "Nombre: " + p[1] + "Especialidad: " + p[2])
        
def darTurno():
    #mostrarProfesionales()

    #idProfesional = input("Ingrese ID profesional: ")
    ok= False #Esto lo quitaba porque no hace nada
    esp = input("Ingrese ID Especialidad \n") #Esto lo cambiaría en lugar de especialidad a por id del profesional (médico) (Qué es esp??)
    print("Ingrese DNI del paciente")
    dni = input()
    print("Ingrese fecha xx/xx/xx")
    fecha = input()
    print("Ingrese hora xx:xx")
    hora = input()
    for p in profesionales: # chequeo si existe el id del profesional ingresado en la lista de profesionales
        if(p[0] == esp):
            turnos.append([dni, fecha, hora]) # por ahora la lista de turnos es global para todos los profesionales #Metería el idProfesional aquí también
            print("Turno dado correctamente") # faltaria chequear antes de dar un turno si no existia un turno ya en ese horario
            return
    print("no se encontró un profesional con id de especialidad ingresada")

def reprogramarTurno():
    dni = input("Ingrese DNI del paciente")
    fecha = input("Ingrese nueva fecha")
    hora = input("Ingrese nueva hora")
    for t in turnos:
        if(t[0] == dni):
            t[1] = fecha
            t[2] = hora
            print("Turno reprogramado") #aca falta chequear tambien si el nuevo horario ya estaba ocupado para no pisar turnos
            return #salir del bucle y no seguir buscando
    print("No se encontró un turno para el DNI del paciente ingresado")

def cancelarTurno():
    print("Ingrese DNI del paciente")
    dni = input()
    for t in turnos:
        if(t[0] == dni):
            turnos.remove(t)
            print("Turno cancelado")
            return #sale del bucle y no sigue buscando al pedo
    print("No se encontró un turno para el paciente ingresado")

def listarTurnos():
    for t in turnos:
        print("Paciente DNI: " + t[0] + " Fecha: " + t[1] + " Hora: " + t[2])

