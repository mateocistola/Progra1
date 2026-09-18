from datetime import datetime
ahora = datetime.now()
fecha = datetime(ahora.year, ahora.month, ahora.day)
#---------------------------------------FUNCIONES---------------------------------------#
def ulti_dos_digit(año): # necesito los ultimos 2 digitos para la formula Doomsday
        num = año // 100
        new = año - num * 100
        return new
def bisiesto():
    if (ahora.year % 4 == 0 and ahora.year % 100 != 0) or (ahora.year % 400 == 0):
        return 29
    return 28
#----------------------------------LISTAS Y VARIABLES----------------------------------#    
meses = [" ","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
sem = ['0','Lu','Ma','Mi','Ju','Vi','Sa','Do']
d_mes = [0,31, bisiesto(), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


dos_digit = ulti_dos_digit(ahora.year)
dia_sem = int((dos_digit+(dos_digit/4))%7)
#------------------------------------PROGRAMA PRINCIPAL----------------------------#

def mostrar_meses ():
    print('-------------------------------')
    print('Mes Actual de',meses[ahora.month])
    for t in range (1,len(sem)): # imprime dia de sem
        print(sem[t], end = '     ')
    print()
    for d in range (dia_sem): #marca el indice del dia en que esta el mes
       print('.',end = '        ')
    s = dia_sem 
    for i in range (ahora.day,d_mes[ahora.month]+1):#empezamos en 1 como todos los meses y agregamos 1 para q no termine antes el ciclo
        if ahora.day <= i:
            if ahora.day < i:
                print(i,end = '      ')
                s = s +1
            elif ahora.day == i:
                print('  X ',end = '      ')
                s = s +1
            if 'Do' == sem[s]:
                print()
                s = 0
    print()
