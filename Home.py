import Turnero
import Profesionales
import Pacientes

def menuPrincipal(profesionales, pacientes, turnos):
    eleccion = 0
    print("Bienvenido -- Sistema de Reserva de Turnos Médicos")
    while eleccion != 7:
        eleccion = input(
            "Ingrese: \n" 
            " 1 para dar turnos. \n"
            " 2 para reprogramar un turno. \n"
            " 3 para cancelar un turno. \n"
            " 4 para listar todos los turnos en sistema. \n"
            " 5 para menú de profesionales. \n"
            " 6 para el menú de pacientes. \n"
            " 7 para salir. \n")
        while not eleccion.isdigit():
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 7:"
            )
        eleccion = int(eleccion)
        match eleccion:
            case 1:
                Turnero.darTurno(profesionales,pacientes, turnos)
            case 2:
                Turnero.reprogramarTurno(turnos)
            case 3:
                Turnero.cancelarTurno(turnos)
            case 4:
                Turnero.listarTodosLosTurnos(turnos)
            case 5:
                Profesionales.menu(profesionales, turnos)
            case 6:
                Pacientes.menu(pacientes)
            case 7:
                print("Saliendo...")
            case _:
                print("Opción incorrecta.")


def main():
    profesionales = [
        ["1", "Perez, Carolina", "Cardiologia", 9, 17],
        ["2", "Gomez, Alejandra", "Clinica Medica", 8, 16],
        ["3", "Lopez, Eduardo", "Traumatologia", 10, 18]  # incluimos profesionales de prueba
    ]
    pacientes = {}
    turnos = []

    menuPrincipal(profesionales, pacientes, turnos)

main()
