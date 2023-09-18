
from deap import base, algorithms, tools


import main


def configura_experimentos():

    experimentos = []
    
    # Se va a comprobar el efecto de aumentar el nº de generaciones del algoritmo
    ngen = [20, 30, 40, 50]
    poblacion = [25, 50, 75, 100]
    probcruce = [0.25,0.5,0.75,1]
    probmut = [0.1, 0.2, 0.5, 1]

    # Los experimentos se van a realizar sobre distintas configuraciones del problema
    data_input = ["./material/input/boat_test01.csv","./material/input/boat_test03.csv","./material/input/boat_test06.csv"]

    for di in data_input:
        """descomentar cada bucle dependiendo del parametro a evaluar"""
        #for n in ngen:
        #for p in poblacion:
        #for pc in probcruce
        for pm in probmut:
                
            exp = {}
        
            exp['data_input'] = di

            alg_param = {}
            alg_param['cxpb'] = 0.25
            #alg_param['cxpb'] = pc
            #alg_param['mutpb'] = 0.2
            alg_param['mutpb'] = pm
            alg_param['pop_size'] = 25
            #alg_param['pop_size'] = p
            #alg_param['ngen'] = n
            alg_param['ngen'] = 50
        
            exp['alg_param'] = alg_param

            experimentos.append(exp)


    return experimentos

# Recibe una lista de diccionarios, cada uno para un experimento
# Va ejecutando uno por uno, almacenando la población final obtenida y sus estadísticas
def ejecuta_experimentos(experimentos, stats):

    populations = []
    logbooks = []
    main.crearFitnesseIndividuo()
    for exp in experimentos:

        main.cargarCSV(exp['data_input'])
        
        # Herramienta para guardar la configuracion de la ejecucion
        toolbox = base.Toolbox()

        # Se configura cómo se define cada individuo. Ver fichero correspondiente
        main.configurarPoblacion(toolbox)

        # Se configura los diferentes esquemas del ciclo evolutivo (tipo de selección, cruce,...)
        # CUIDADO: Hay que tener en cuenta que la configuración que se crea en esta llamada, se sobreescribe
        # al utilizar la configuración guardada en alg_param y utilizar sus parámetros en eaSimple
        main.configuracionAlgoritmo(toolbox)
        # Por simplificar se emplea la configuración de otros ejemplos, pero se 
        # puede variar a la hora de configurar los experimentos (y comparar 2 tipos de cruce, p.ej.)

        alg_param = exp['alg_param']

        # Inicialización de la población
        init_pop = toolbox.population(n=alg_param['pop_size'])

        # Ejecución de la evolucion
        population, logbook = algorithms.eaSimple(
            init_pop, toolbox, 
            cxpb=alg_param['cxpb'], 
            mutpb=alg_param['mutpb'], 
            ngen=alg_param['ngen'], 
            verbose=True, stats=stats)

        populations.append(population)
        logbooks.append(logbook)
    
    return populations, logbooks

def visualiza_experimentos(experimentos, populations, logbooks):

    for exp, pop, log in zip(experimentos, populations, logbooks):

        print("Parametros del experimento: ")
        print(exp)
        
        print("La mejor solucion encontrada es: ")
        print(tools.selBest(pop,1)[0])
        
        print("Que tiene una valoración de: ")
        print(tools.selBest(pop,1)[0].fitness)

        main.mostrarGrafica(log)

if __name__ == "__main__":
    experimentos = configura_experimentos()
    stats = main.getStats()
    pops,logs = ejecuta_experimentos(experimentos,stats)
    visualiza_experimentos(experimentos, pops,logs)