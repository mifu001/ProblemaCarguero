import random
import math
from deap import base, creator
from deap import tools
from deap import algorithms
import util
import modelo
import multiprocessing
import numpy
import matplotlib.pyplot as plt


def getStats():
    # Se configura que estadísticas se quieren analizar
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    return stats
def crearFitnesseIndividuo():
    #definimos el fitness, y definimos que el mejor individuo es el que mayor fitness tenga.
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

def realizaEvolucion(toolbox, stats,file):
    
    crearFitnesseIndividuo()
    configurarPoblacion(toolbox)

    configuracionAlgoritmo(toolbox)
    stats = getStats()
    #decimos el numero de individuos que tiene una poblacion
    population = toolbox.population(n=100)
    #hace la evolución con los parametros introducidos
    population, logbook = algorithms.eaSimple(population, toolbox,
	                               cxpb=0.5, mutpb=0.4,
	                               ngen=50, verbose=True, stats=stats)


    print("El resultado de la evolución es: ")
    print(logbook)
    mostrarGrafica(logbook)


    print("La mejor solucion encontrada es: ")
    #imprimimos el fenotipo del individuo con mejor resultado
    print(tools.selBest(population,1)[0])
    #imprimimos el valor que se le ha dado al individuo
    print(evaluarIndividuos(tools.selBest(population,1)[0]))
    #escribimos en el CSV los compartimentos del barco
    util.writeCSV(file,__numCompartimentos__,len(__listaContenedores__),__contenedoresXCompartimento__,tools.selBest(population,1)[0])
    #obtenemos los barcos para imprimirlos en el archivo outout.txt
    outputId = util.printBarcoFromList(tools.selBest(population,1)[0], __numCompartimentos__, math.ceil(math.sqrt(__contenedoresXCompartimento__)), __listaContenedores__, "id")
    outputPeso = util.printBarcoFromList(tools.selBest(population,1)[0], __numCompartimentos__, math.ceil(math.sqrt(__contenedoresXCompartimento__)), __listaContenedores__, "peso")
    outputPuerto = util.printBarcoFromList(tools.selBest(population,1)[0], __numCompartimentos__, math.ceil(math.sqrt(__contenedoresXCompartimento__)), __listaContenedores__, "puerto")
    with open("output.txt", "w") as file:
        file.write(outputId)
        file.write(outputPeso)
        file.write(outputPuerto)
    plt.show()
    return logbook
    # return logbook
def mostrarGrafica(logbook):
    gen = logbook.select("gen")
    avgs = logbook.select("avg")
    maxim = logbook.select("max")
    minim = logbook.select("min")

    # Se establece una figura para dibujar
    fig = plt.figure()

    # Se representa la media del valor de fitness por cada generación
    ax1 = plt.gca()

    line1 = ax1.plot(gen, maxim, "r-", label="Max Fitness")
    ax1.set_xlabel("Generation")
    ax1.set_ylabel("Max Fitness", color="r")
    plt.show()
    # Se representa la media del valor de fitness por cada generación
    ax2 = plt.gca()

    line2 = ax2.plot(gen, minim, "g-", label="Min Fitness")
    ax2.set_xlabel("Generation")
    ax2.set_ylabel("Min Fitness", color="g")
    plt.show()
    # Se representa la media del valor de fitness por cada generación
    ax3 = plt.gca()
    line3 = ax3.plot(gen, avgs, "b-", label="Avg Fitness")
    ax3.set_xlabel("Generation")
    ax3.set_ylabel("Fitness", color="b")
    plt.show()



def configurarPoblacion(toolbox):

    try:
        pool = multiprocessing.Pool(24)
        toolbox.register("map", pool.map)
    except:
        print("No usando multiproceso :S")

    #decimos que el genotipo es de tipo getBarcoValidoFinal, que es un barco aleatorio
    toolbox.register("indices", util.getBarcoValidoFinal,barco=__Barco__,contenedores=__listaContenedores__)
    #hacemos iteraciones de los indices de esta forma, no se deberian repetir los indices
    toolbox.register("individual", tools.initIterate, creator.Individual,toolbox.indices)
    #Y por ultimo declaramos la poblacion como una lista de individuos.
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def configuracionAlgoritmo(toolbox):
    #Escogemos de crossover el PartialyMatched, que utiliza un algoritmo que evita ciclos, y de esta forma, no se repiten los indices.
    toolbox.register("mate", tools.cxOrdered)
    # Mutaciones lo que hacemos es que mueva los indices.
    toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2)
    # El algoritmo de seleccion, hacemos que sea toneo, de tamaño 5
    toolbox.register("select", tools.selTournament, tournsize=5)
    #Y evaluamos los individuos.
    toolbox.register("evaluate",   evaluarIndividuos)

def evaluarIndividuos(individual):
    #valor optimo para los programas sera 0, puesto que solo se hace una operacion de resta.

    value = 0

    altura=int(math.sqrt(__contenedoresXCompartimento__))
    puertos = []
    pesos = []
    # recorremos los individuos, para añadir los pesos y los puertos de los contenedores vacios
    for valor in individual:
        if(valor == -1):
            puertos.append(-1)
            pesos.append(-1)
        else:
            puertos.append(__listaContenedores__[valor].puerto)
            pesos.append(__listaContenedores__[valor].peso)
    #recorremos los individuos, para comprobar si un individuo que no sea "contenedor vacio" esta repetido o falta.
    for i in range(len(__listaContenedores__)):
        if(individual.count(i)!=1):
            value -= 10000 * len(individual)
            
    pesosCompartimentos=[]
    #para que no se hunda el barco, sumamos los pesos de cada contendor.
    for i in range(__numCompartimentos__):
        pesosCompartimentos.append(sum(pesos[i*__contenedoresXCompartimento__:(i+1)*__contenedoresXCompartimento__]))

    pesoComparIzq = sum(pesosCompartimentos[:math.floor(__numCompartimentos__/2)])
    pesoComparDer = sum(pesosCompartimentos[math.ceil(__numCompartimentos__/2):])
    #comparamos el lado izquierdo y el lado derecho para comprobar la diferencia
    if(abs(pesoComparDer - pesoComparIzq) > 1000):
        value = value - 5000
    #por cada valor del barco, comprobamos su posicion respecto al compartimento y el valor que se va a restar.
    for i in range(len(individual)):
        posicion = i % __contenedoresXCompartimento__
        valorMedioRestar = ((__contenedoresXCompartimento__/altura)-math.floor(posicion/altura))
        #si no es la fila mas alta  del compartimento
        if(posicion+altura<__contenedoresXCompartimento__):
            #si el contenedor actual es vacio, y el de encima no lo es, restamos.
            if(pesos[i] == -1 and pesos[i+altura] > -1):
                value = value - (100*valorMedioRestar)
            #si el contenedor actual pesa menos que el de encima, restamos
            if(pesos[i] - pesos[i+altura] < 0):
                value = value - (1000*valorMedioRestar)
            # comparamos los puertos del actual con el de arriba, si hay que mover el de arriba para sacar este, restamos.
            diff = puertos[i] - puertos[i+altura]
            if(diff<0):
                value = value - (valorMedioRestar)*50
        else:
            #si fila de arriba no tiene -1, restamos,
            # esto lo hacemos asi, para preferir soluciones a lo ancho que a lo alto. Ya que se mantiene mejor en equilibrio 
            if(pesos[i] != -1 ):
                value = value - 1
    return (value,)

def cargarCSV(archivo):
    global __Barco__
    global __numCompartimentos__
    global __listaContenedores__
    global __totalConHuecos__
    global __contenedoresXCompartimento__

    (__Barco__,__listaContenedores__,__numCompartimentos__, __totalConHuecos__,__contenedoresXCompartimento__) = util.loadCSV(archivo)
    



def main(toolbox, x):

    archivo ="./material/input/boat_test0"+str(x)+".csv"
    file = "./material/output/boat_result0"+str(x)+".csv"
    cargarCSV(archivo)
    realizaEvolucion(toolbox,[],file)



if __name__ == "__main__":
    print("Introduce un numero del 1 al 6 para seleccionar el archivo en concreto")
    x = int(input())
    if(x>6 or x<1):
        x=1
        print("numero incorrecto, se escogera por defecto el archivo 1")
    toolbox = base.Toolbox()
    main(toolbox, x)
