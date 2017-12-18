#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import sys
import os
sys.path.append('./classes/')
from createnetwerk import createNetwerk
from ScoreVariables import score_variables
from Scorefromroute import scorefromroute
sys.path.append('./functions/')
from Score import score
from Histogram import histogram
sys.path.append('./algorithms/')
from Breadth_first import breadth_first_route
from Greedy import greedy
from Visualization  import visualization
from Random_search	import random_route
#from Hillclimber    import hillclimber
import matplotlib.pyplot as plt



def main():
    
#    trainamount = int(input("Amount Trains [Int]: "))
#    trials = int(input("Amount Trials [Int]: "))
#    Usage2 = int(input("Holland/Nationaal [Holland = 0; Nationaal = 1]: "))
#    Usage3 = int(input("Random [No = 0; Yes = 1]]: "))
#    Usage4 = int(input("BreadFirst [No = 0; Yes = 1]: "))
#    Usage5 = int(input("HillClimber [No = 0; Yes = 1]: "))
#    Usage6 = int(input("Greedy [No = 0; Yes = 1]: "))
#    Usage7 = int(input("Plot [No = 0; Yes = 1]: "))

    trainamount = 7
    trials = 100
    Usage2 = 0
    Usage3 = 0
    Usage4 = 0
    Usage5 = 0
    Usage6 = 1
    Usage7 = 0
        
    if Usage2 == 0:
        x = createNetwerk('./csv/StationsHolland.csv', './csv/ConnectiesHolland.csv')
    if Usage2 ==  1:
        x = createNetwerk('./csv/StationsNationaal.csv', './csv/ConnectiesNationaal.csv')

    if Usage3 == 1:
        for i in range(trials):
            # random search
            visited_connections, route = random_route(x.array, x.starting_stations, x.stations)
            for row in route:
                print(row)
    
    if Usage4 == 1:
        # breadth first
        route, score = breadth_first_route(x.array, x.stations, x.critical, trainamount, trials)
        for row in route:
            print(row)

    if Usage6 == 1:
        # greedy
        route = greedy(x.connections, x.criticalconnections, x.critical, trainamount, trials)
        for row in route:
            print(row)
        greedyscore = scorefromroute(route, x.connections, trainamount)
        print(greedyscore)
#        histogram('Greedy','./csv/greedyalltrials.csv')

#    object = score_variables()
#    # score function parameters
#    p    = object.p(x.array, visited_connections, x.stations, x.critical)
#    t   = object.t(visited_connections)
#    min = object.min(route)
# scorefunctie

#
#    print(connectioncheck1)
#    connectioncheck2 = []
#    for connection in x.connections:
#    for check in connectioncheck1:
#        print(check)
#            print(check[0])
#            print(check[1])
#            if check[0] in connection:
#                if check[1] in connection:
#                    if connection not in connectioncheck2:
#                        connectioncheck2.append([connection[0:2]])
#            if check[0] == connection[1]:
#                if check[1] == connection[0]:
#                    if connection not in connectioncheck2:
#                        connectioncheck2.append([connection[0:2]])
#    print("")
#    print(connectioncheck2)
#    print("")
#    print(x.connections)
#
    if Usage7 == 1:
        # create and print visualization
        visualization(x.longitude, x.latitude, x.stations, route, x.critical, x.array, 2000)

if __name__ == "__main__":
    main()

