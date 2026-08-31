from datetime import datetime



def dias_de_semana():
    for d in range(len(sem)):# dias_de_semana 
        print(sem[d], end = ' 	')
    print('')

''' def elijo_turn():
    print()
    print()
    diaT=int(input('Ingrese el Numero del dia que desea el Turno (ejemplo 12 = lunes): '))
    print()
    mesT=int(input('Ingrese el Numero del mes que desea el Turno (ejemplo 8 = agosto ): '))
    return diaT,mesT,ahora.year
'''
dias = ["lunes","martes","miércoles","jueves","viernes","sábado","domingo"]
sem = ['Lu','Ma','Mi','Ju','Vi','Sa','Do']
meses = [" ","Enero","Febrero","Marzo","Abril","Mayo","Junio","Julio","AGOSTO","SEPTIEMBRE","OCTUBRE","NOVIEMBRE","DICIEMBRE"]

ahora = datetime.now()
fecha = datetime(ahora.year, ahora.month, ahora.day)
'''print(dias[fecha.weekday()]) # imprime el dia de la semana '''

def mostrar_meses ():
    print()
 #mostramos el mes con dias disponibles 
    print('	MES DE ',meses [ahora.month],'(',ahora.month ,')')

# imprimir mes actual
    dias_de_semana()

    for i in range(ahora.day+1):
        if i % 7 == 0 and i != 0:
            print(i )
        elif i !=0:
            print(i, end = '	 '  )       
    print()
    print()

# imprimir proximo mes 
    print('	MES DE ',meses [ahora.month + 1],'(',ahora.month + 1,')')

    dias_de_semana()
    for x in range(ahora.day):
        if x % 7 == 0 and x != 0:
            print(x )
        elif x !=0:
            print(x, end = '	 '  )
    print()


    

