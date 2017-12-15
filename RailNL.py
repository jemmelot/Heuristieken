#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import sys
import os
sys.path.append('./classes/')
from createnetwerk import createNetwerk
from ScoreVariables import score_variables
sys.path.append('./functions/')
from Score import score
sys.path.append('./algorithms/')
from Breadth_first import breadth_first_route
from Greedy import greedy
from Visualization  import visualization
from Random_search	import random_route
#from Hillclimber    import hillclimber
import matplotlib.pyplot as plt




def main():
    
    Usage0 = int(input("Amount Trains [Int]: "))
    Usage1 = int(input("Amount Trials [Int]: "))
    Usage2 = int(input("Holland/Nationaal [Holland = 0; Nationaal = 1]: "))
    Usage3 = int(input("Random [No = 0; Yes = 1]]: "))
    Usage4 = int(input("BreadFirst [No = 0; Yes = 1]: "))
    Usage5 = int(input("HillClimber [No = 0; Yes = 1]: "))
    Usage6 = int(input("Greedy [No = 0; Yes = 1]: "))
    Usage7 = int(input("Plot [No = 0; Yes = 1]: "))
    
    for i in range(Usage1):
        
        if Usage2 == 0:
            x = createNetwerk('./csv/StationsHolland.csv', './csv/ConnectiesHolland.csv')
        if Usage2 ==  1:
            x = createNetwerk('./csv/StationsNationaal.csv', './csv/ConnectiesNationaal.csv')

        if Usage3 == 1:
            # random search
            visited_connections, route = random_route(x.array, x.starting_stations, x.stations)
            for row in route:
                print(row)
        
        if Usage4 == 1:
            # breadth first
            route, all_time_highest_score = breadth_first_route(x.array, x.starting_stations, x.stations, x.critical)
            for row in route:
                print(row)

    #    if Usage5 == 1:
    #        # hill-climber
    #        #hc_score = hillclimber(evaluations)

        if Usage6 == 1:
            # greedy
            route = greedy(x.connections, x.criticalconnections, x.critical, Usage0, Usage1)
            for row in route:
                print(row)
    
    # route = copy.deepcopy.route
    # labels op asses PUNTEN
#    object = score_variables()
#    # score function parameters
#    p    = object.p(x.array, visited_connections, x.stations, x.critical)
#    t   = object.t(visited_connections)
#    min = object.min(route)

    if Usage7 == 1:
        # create and print visualization
        visualization(x.longitude, x.latitude, x.stations, route, x.critical, x.array, 2000)

if __name__ == "__main__":
    main()

