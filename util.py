from modelo import Barco, Contenedor
from random import shuffle, randint
import math
import csv

def loadCSV(path) :
    csvFile = open(path, "r")
    lines = [row.split(',') for row in csvFile.readlines()]
    comparts = int(lines[0][0])
    conts = int(lines[0][1])/comparts

    alto = math.ceil(math.sqrt(conts))
    ancho = alto
    barco = Barco(comparts, ancho, alto)

    contenedores = [Contenedor(line[0], float(line[1]), int(line[2]), bool(int(line[3]))) for line in lines[1:]]
    
    contenedoresXCompartimento = alto*ancho
    totalConHuecos = alto*ancho*comparts
    csvFile.close()

    return (barco, contenedores,comparts,totalConHuecos,contenedoresXCompartimento)

#funcion que determina al programa obtener un barco con los contenedores vacios en la parte de arriba
#si se descomenta el sort de la lista, se obtiene un genotipo de barco valido, donde solo se podrian mejorar el orden de los puertos
def getBarcoValidoFinal(barco: Barco, contenedores: list[Contenedor]):
    compartimentos = len(barco.compartimentos)
    ancho = barco.compartimentos[0].ancho
    alto = barco.compartimentos[0].alto
    lista = []
    listaFinal = [-1 for i in range(compartimentos*ancho*alto)]
    for i in range(len(contenedores)):
        lista.append((i,contenedores[i]))
    
    # lista.sort(key=lambda a: a[1],reverse = True)
    listaPosicionesValidas = []
    for i in range(compartimentos):
        for j in range(alto):
            listaPosicionesValidas.append([0,j+(alto*ancho*i)])
    
    for i in range(len(contenedores)):
        variable = True
        while(variable):
            valor = randint(0,len(listaPosicionesValidas)-1)
            if(listaPosicionesValidas[valor][0]<alto):
                variable = False
        posicion = listaPosicionesValidas[valor][1]
        listaFinal[posicion] = lista[i][0]
        listaPosicionesValidas[valor][0] += 1
        listaPosicionesValidas[valor][1] += alto
    return listaFinal

#escribimos el mejor caso, en el csv de salida    
def writeCSV(path,comp,cont,contXComp,mejorResultado):
    csvFile = open(path, "w",newline='')
    writer = csv.writer(csvFile)
    writer.writerow([comp,cont])

    for i in range(comp):
        writer.writerow(mejorResultado[(i*contXComp):((i+1)*(contXComp))])
    csvFile.close()



# Dado el compartimento, la fila y la columna devuelve el índice
def posToIndice(comp:int, fila:int, columna:int, dims: int):
    return (fila * dims + columna) + (dims * dims * comp)

# Imprimimos el barco en el fichero output.txt segun el parametro introducido
def printBarcoFromList(lista: list[Contenedor], numComp:int, dims:int, listaContenedores: list[Contenedor], modo:str):
    # id, peso, puerto
    metodos = [Contenedor.peso, Contenedor.puerto]
    function: function = lambda j, i, k, dims: lista[posToIndice(j, i, k, dims)]
    if modo == "id":
        function = lambda j, i, k, dims: lista[posToIndice(j, i, k, dims)]
    elif modo == "peso":
        function = lambda j, i, k, dims: int(listaContenedores[lista[posToIndice(j, i, k, dims)]].peso) if lista[posToIndice(j, i, k, dims)] != -1 else -1
    elif modo == "puerto":
        function = lambda j, i, k, dims: listaContenedores[lista[posToIndice(j, i, k, dims)]].puerto if lista[posToIndice(j, i, k, dims)] != -1 else -1




    output = "\n\n" + modo + ":\n"
    bandera = "\n|-------------\n|            (\n|             )\n|            (\n|             )\n|--------------\n|\n|\n|\n|\n|\n|\n|"
    output += bandera.replace("\n", "\n     ")
    output += "\n"
    for i in range(dims - 1, -1, -1):
        for j in range(((dims - 1) - i) + 5):
            output += " "
        
        output += "\\"
        for j in range(i):
            
            output += " "
        
        output += "|"
        for j in range(numComp):
            for k in range(dims):
                
                output += "{0: >4} ".format(str(function(j, i, k, dims)))
            
            output += "|"
        for j in range(i):
            
            output += " "
        
        output += "/"
        for j in range(((dims - 1) - i + 5)):
            
            output += " "
        
        output += "\n"

    for i in range(dims + 5):
        output += "~"
    output += "\\"
    for i in range(dims * numComp * 5 + (numComp - 1)):
        output += "_"
    output += "/"
    for i in range(dims + 5):
        output += "~"

    
    output += "\n"
    for j in range(5):
        for i in range(dims + 5 + (dims * numComp * 5 + (numComp - 1)) + dims + 5):
            if randint(0, 20) == 0:
                output += "~"
            else:
                output += " "
        output += "\n"
    
    return output
