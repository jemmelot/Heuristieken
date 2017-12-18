#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import sys
import os
sys.path.append('./classes/')
from createnetwerk import createNetwerk
from Scorefromroute import score_from_route
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
#    map = int(input("Holland/Nationaal [Holland = 0; Nationaal = 1]: "))
#    random_search = int(input("Random [No = 0; Yes = 1]]: "))
#    breadth_first = int(input("BreadFirst [No = 0; Yes = 1]: "))
#    hillclimber = int(input("HillClimber [No = 0; Yes = 1]: "))
#    greedy = int(input("Greedy [No = 0; Yes = 1]: "))
#    visualisatie = int(input("Plot [No = 0; Yes = 1]: "))

    trainamount = 7
    trials = 1
    map = 0
    use_random_search = 1
    use_breadth_first = 0
    use_hillclimber = 0
    use_greedy = 0
    use_visualisatie = 0
        
    if map == 0:
        x = createNetwerk('./csv/StationsHolland.csv', './csv/ConnectiesHolland.csv')
    if map ==  1:
        x = createNetwerk('./csv/StationsNationaal.csv', './csv/ConnectiesNationaal.csv')

    if use_random_search:
        print(x.connections)
        # random search
        random_search_route = random_route(x.array, x.starting_stations, x.stations, trainamount, trials)
        for row in random_search_route:
            print(row)
        random_search_score_from_route = score_from_route(random_search_route, x.connections, trainamount)
        print(random_search_score_from_route)
    
    if use_breadth_first:
        # breadth first
        breadth_first_route, breadth_first_score = breadth_first_route(x.array, x.starting_stations, x.stations, x.critical, trainamount, trials)
        for row in breadth_first_route:
            print(row)
        bread_first_score_from_route = score_from_route(route, x.connections, trainamount)

    if use_greedy:
        # greedy
        greedy_route = greedy(x.connections, x.criticalconnections, x.critical, trainamount, trials)
        for row in greedy_route:
            print(row)
        greedy_score_from_route = score_from_route(greedy_route, x.connections, trainamount)
        print(greedy_score_from_route)
        histogram('Greedy','./csv/greedyalltrials.csv')

    if use_visualisatie:
        # create and print visualization
        visualization(x.longitude, x.latitude, x.stations, route, x.critical, x.array, 2000)

if __name__ == "__main__":
    main()

