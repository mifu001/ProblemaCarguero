# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 11:47:43 2020

@author: bbaruque
"""

import math

num_cmp = 0
num_cont_comp = 0

def load_solution(file):

    in_file = open (file, "r")
    content_lines = in_file.readlines()
    in_file.close()

    num_cmp = int(content_lines[0].split(",")[0])

    print("La solución incluye {} compartimentos".format(num_cmp))
    
    # Comprobando numero de líneas en el fichero
    assert (len(content_lines[1:]) == num_cmp), "ERROR: El numero de compartimentos incluido en la respuesta no concuerda."

    num_cont_comp = len(content_lines[1].split(","))

    solution = []

    for cn, line in enumerate(content_lines[1:]):
        
        line = line.split(",")
        
        assert len(line) == num_cont_comp, "ERROR: el numero de contenedores es diferente en diferentes líneas."
        assert math.sqrt(len(line))%1 == 0 , "ERROR: el numero de contenedores es diferente en diferentes líneas."
            
        l_int = list(map(int, line))
        
        print("Compartimento {} - Contenido (de izq. a der, de abajo a arriba): {}".format(cn,l_int))
        
        solution.extend(l_int)
        
    return solution


#%%
if __name__ == "__main__":
    
    file = "./material/output/boat_result02.csv"
    sol = load_solution(file)
    
