#Sistema de Reserva de Turnos Médicos
#Implementar un sistema que gestione la reserva de turnos médicos para los profesionales de las distintas especialidades que atiende un centro de salud, utilizando
#matrices, listas y diccionarios para mantener la información, almacenándola en archivos para permitir su posterior recuperación. Aplicar recursividad para realizar las
#búsquedas de una manera ágil y flexible.
import Turnero;

print("Bienvenido -- Sistema de Reserva de Turnos Médicos")

print("¿Que desea hacer?")
print("Ingrese: 1 para dar turnos, 2 para reprogramar un turno, 3 para cancelar un turno, 4 para listar los turnos de un paciente")
eleccion = int (input())
if eleccion == 1:
    Turnero.darTurno
else:
    if eleccion == 2:
        Turnero.reprogramarTurno
    else:
        if eleccion == 3:
            Turnero.cancelarTurno
        else:
            if eleccion == 4:
                Turnero.listarTurnos
            else:
                print("Ingresa una opcion valida.")