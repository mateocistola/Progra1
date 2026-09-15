import Profesionales; #separación de responsabilidades, cada módulo tiene su propia responsabilidad

turnos = [

]

def darTurno():
    print("Seleccione un profesional...")
    Profesionales.mostrarProfesionales()
    matricula = input("Ingrese Matricula del profesional: ")
    dni = input("Ingrese DNI del paciente: ")
    fecha = input("Ingrese fecha xx/xx/xx: ")
    hora = input("Ingrese hora xx:xx: ")
    for profesional in Profesionales.profesionales: # chequeo si existe el id del profesional ingresado en la lista de profesionales
        if(profesional[0] == matricula):
            for turno in turnos: # chequeo si ya existe un turno para el mismo paciente en la misma fecha y hora
                if(turno[1] == fecha and turno[2] == hora and turno[3] == matricula):
                    print("Ya existe un turno para el profesional en la fecha y hora ingresadas")
                    return
            
            turnos.append([dni, fecha, hora, matricula])
            print("Turno dado correctamente")
            listarTurnos()
            return
    print("no se encontró un profesional con id de especialidad ingresada")

def reprogramarTurno():
    dni = input("Ingrese DNI del paciente: ")
    fecha = input("Ingrese nueva fecha: ")
    hora = input("Ingrese nueva hora: ")
    for turno in turnos:
        if(turno[0] == dni):
            print("Turno a reprogramar encontrado: Fecha: " + turno[1] + " Hora: " + turno[2])
            for turno2 in turnos: # chequeo si ya existe un turno para el mismo paciente en la misma fecha y hora
                if(turno2[1] == fecha and turno2[2] == hora and turno2[3] == turno[3]): #turno2[3] es el id del profesional del turno que se quiere reprogramar, turno[3] es el id del profesional
                    print("Ya existe un turno para el profesional en la fecha y hora ingresadas. \n Los horarios disponibles para el profesional son: ")
                    for turno3 in turnos:
                        if(turno3[3] == turno[3]):
                            print("Fecha: " + turno3[1] + " Hora: " + turno3[2])
                    return
            turno[1] = fecha
            turno[2] = hora
            print("Turno reprogramado: Fecha: " + turno[1] + " Hora: " + turno[2]) #aca falta chequear tambien si el nuevo horario ya estaba ocupado para no pisar turnos
            return #salir del bucle y no seguir buscando
    print("No se encontró un turno para el DNI del paciente ingresado")

def cancelarTurno():
    print("Ingrese DNI del paciente: ")
    dni = input()
    for turno in turnos:
        if(turno[0] == dni):
            turnos.remove(turno)
            print("Turno cancelado")
            return #sale del bucle y no sigue buscando al pedo
    print("No se encontró un turno para el paciente ingresado")

def listarTurnos():
    print("Los turnos agendados son: ")
    if turnos.__len__() == 0:
        print("No hay turnos agendados")
        return
    
    for turno in turnos:
        print("Paciente DNI: " + turno[0] + " Fecha: " + turno[1] + " Hora: " + turno[2])