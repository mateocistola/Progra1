import Turnero
import Profesionales
import Pacientes
import Especialidades

def menuPrincipal(profesionales, pacientes, turnos, especialidades):
    eleccion = 0
    print("Bienvenido -- Sistema de Reserva de Turnos Médicos")
    while eleccion != 8:
        eleccion = input(
            "Ingrese: \n" 
            " 1 para dar turnos. \n"
            " 2 para reprogramar un turno. \n"
            " 3 para cancelar un turno. \n"
            " 4 para listar todos los turnos en sistema. \n"
            " 5 para menú de profesionales. \n"
            " 6 para el menú de pacientes. \n"
            " 7 para el menú de especialidades. \n"
            " 8 para salir. \n"
        )
        while not eleccion.isdigit():
            print("Opción incorrecta.")
            eleccion = input("Ingrese una opción entre 1 y 8:"
            )
        eleccion = int(eleccion)
        match eleccion:
            case 1:
                Turnero.darTurno(profesionales,pacientes, turnos, especialidades)
            case 2:
                Turnero.reprogramarTurno(profesionales, turnos)
            case 3:
                Turnero.cancelarTurno(turnos)
            case 4:
                Turnero.listarTodosLosTurnos(turnos)
            case 5:
                Profesionales.menu(profesionales, turnos, especialidades)
            case 6:
                Pacientes.menu(pacientes)
            case 7:
                Especialidades.menu(especialidades, profesionales)
            case 8:
                print("Saliendo...")
            case _:
                print("Opción incorrecta.")


def main():
    #Cada profesional se guarda en una lista con su legajo,
    #su nombre, especialidad y horarios de atención.
    #Los horarios se organizan en un diccionario por día.
    #Una lista vacía significa que el profesional no atiende
    profesionales = [
        ["1", "Perez, Carolina", "Cardiología",
         {"lunes": ["09:00", "13:00"],
          "martes":["15:00", "19:00"],
          "miércoles": ["09:00", "13:00"],
          "jueves": ["15:00", "19:00"],
          "viernes": ["09:00", "13:00"],
          "sábado": [],
          "domingo": []}, 20 #Duración de cada turno
        ],
        ["2", "Gomez, Alejandra", "Clínica Medica",
         {
             "lunes": ["08:00","12:00"],
             "martes":["08:00","12:00"],
             "miércoles":[],
             "jueves":["14:00","18:00"],
             "viernes":["14:00","18:00"],
             "sábado":[],
             "domingo":[]
         }, 20 #Duración de cada turno
        ],
        ["3", "Lopez, Eduardo", "Traumatología",
         {"lunes": ["10:00","14:00"],
          "martes":[],
          "miércoles":["10:00","14:00"],
          "jueves":["16:00","20:00"],
          "viernes":["10:00","14:00"],
          "sábado":[],
          "domingo":[]
          }, 20 #Duración de cada turno
        ]  # incluimos profesionales de prueba
    ]

    especialidades = ["Cardiología", "Clínica Medica", "Traumatología"]

    #Los pacientes se guardan en un diccionario utilizando el legajo como clave
    pacientes = {}
    #Cada turno guarda el legajo del paciente, el legajo del profesional, la fecha y la hora
    turnos = []

    menuPrincipal(profesionales, pacientes, turnos, especialidades)

main()
