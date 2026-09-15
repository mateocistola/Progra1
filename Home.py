#Sistema de Reserva de Turnos Médicos
#Implementar un sistema que gestione la reserva de turnos médicos para los profesionales de las distintas especialidades que atiende un centro de salud, utilizando
#matrices, listas y diccionarios para mantener la información, almacenándola en archivos para permitir su posterior recuperación. Aplicar recursividad para realizar las
#búsquedas de una manera ágil y flexible.

import Turnero, Profesionales;
eleccion = 0
print("Bienvenido -- Sistema de Reserva de Turnos Médicos")
while eleccion != 6:
    eleccion = int (input(
    "Ingrese: \n" 
    " 1 para dar turnos \n"
    " 2 para reprogramar un turno \n"
    " 3 para cancelar un turno \n"
    " 4 para listar los turnos de un paciente \n"
    " 5 para menu de edicion de profesionales \n"
    " 6 para salir \n"))

    match eleccion:
        case 1 :
            Turnero.darTurno()
        case 2:
            Turnero.reprogramarTurno()
        case 3:
            Turnero.cancelarTurno()
        case 4:
            Turnero.listarTurnos()
        case 5:
            Profesionales.menu()
        case 6:
            print("Saliendo...")
        case _:
            print("Opción inválida.")