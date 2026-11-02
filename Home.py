import Turnero
import Profesionales
import Pacientes
import Especialidades


def menuPrincipal():
    eleccion = 0
    print("Bienvenido -- Sistema de Reserva de Turnos Médicos")

    while eleccion != 10:
        eleccion = input(
            "Ingrese: \n"
            " 1 para dar turnos. \n"
            " 2 para reprogramar un turno. \n"
            " 3 para cancelar un turno. \n"
            " 4 para listar todos los turnos históricos del sistema. \n"
            " 5 para listar los turnos del día de un profesional.  \n"
            " 6 para listar los turnos históricos de un paciente. \n"
            " 7 para menú de profesionales. \n"
            " 8 para menú de pacientes. \n"
            " 9 para menú de especialidades. \n"
            "10 para salir. \n"
        )

        while not eleccion.isdigit() or int(eleccion) < 1 or int(eleccion) > 10:
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 10: ")

        eleccion = int(eleccion)

        match eleccion:
            case 1:
                Turnero.darTurno()
            case 2:
                Turnero.reprogramarTurno()
            case 3:
                Turnero.cancelarTurno()
            case 4:
                Turnero.listarTodosLosTurnos()
            case 5:
                Profesionales.listarTurnosDelDia()
            case 6:
                Turnero.listarTurnosDePaciente()
            case 7:
                Profesionales.menu()
            case 8:
                Pacientes.menu()
            case 9:
                Especialidades.menu()
            case 10:
                print("Saliendo...")


def main():
    # Cada módulo administra su propia persistencia:
    # especialidades.json y los archivos TXT secuenciales.
    # La primera ejecución crea las especialidades iniciales si hace falta.
    Especialidades.cargarEspecialidades()
    menuPrincipal()


main()
