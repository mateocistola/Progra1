import Turnero, Profesionales;
eleccion = 0
print("Bienvenido -- Sistema de Reserva de Turnos Médicos")
while eleccion != 6:
    eleccion = int (input(
    "Ingrese: \n" 
    " 1 para dar turnos. \n"
    " 2 para reprogramar un turno. \n"
    " 3 para cancelar un turno. \n"
    " 4 para listar todos los turnos en sistema. \n"
    " 5 para menu de edicion de profesionales. \n"
    " 6 para salir. \n"))

    match eleccion:
        case 1 :
            Turnero.darTurno()
        case 2:
            Turnero.reprogramarTurno()
        case 3:
            Turnero.cancelarTurno()
        case 4:
            Turnero.listarTodosLosTurnos()
        case 5:
            Profesionales.menu()
        case 6:
            print("Saliendo...")
        case _:
            print("Opción incorrecta.")