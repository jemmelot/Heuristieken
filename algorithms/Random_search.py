#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import sys
import csv
import os
sys.path.append('../classes/')
from createnetwerk import createNetwerk
from ScoreIntegrated import score_integrated

def random_route(array, starting_stations, stations, critical_station, trains_amount, trials):
    """Calculates routes at random."""

    with open('./csv/randomsearchscores.csv', 'w') as myfile:
        wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
        wr.writerow([00000.00])
    with open('./csv/randomsearchroute.csv', 'w') as myfile:
        wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
        wr.writerow("00000")
    with open('./csv/randomsearchalltrials.csv', 'w') as myfile:
        wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
        wr.writerow([00000.00])
        
    for trial in range(trials):
        # the seven calculated routes will be stored in this variable
        route = [[] for i in range(trains_amount)]

        # instantiate numpy array to keep track of how often every station is visited
        visited_connections = np.zeros((len(stations), len(stations)))

        # create seven random routes
        for i in range(trains_amount):
            total_time = 0

            rnd = np.random.choice(starting_stations)
            starting_station = stations.index(rnd)
            route[i].append(stations[starting_station])

            def routes(starting_station, total_time):
                x = np.where(array[starting_station, :] > 0)
                r = np.random.choice(x[0])

                if (total_time + array[starting_station][r]) > 120:
                    route[i].insert(0, int(total_time))
                
                else:
                    route[i].append(stations[r])
                    total_time += array[starting_station][r]
                    visited_connections[starting_station][r] += 1
                    visited_connections[r][starting_station] += 1
                    routes(r, total_time)

            routes(starting_station, total_time)
        
        totalscore = float(score_integrated(array, visited_connections, stations, route, critical_station,trains_amount))
        print("")
        print ("Random Search Trial: ", trial)
        with open('./csv/randomsearchscores.csv', 'r') as myfile:
            last_line = myfile.readlines()[-1]
            last_line = float(last_line.rstrip('\n'))

        print ("Highest Score: ", last_line)
        print ("Current Score: ", totalscore)

        if totalscore > last_line:
            print("Result: Succes")
            with open('./csv/randomsearchscores.csv', 'a') as myfile:
                wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
                wr.writerow([totalscore])
            with open('./csv/randomsearchroute.csv', 'a') as myfile:
                wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
                wr.writerow([route])
        else:
            print("Result: Fail")

        with open('./csv/randomsearchalltrials.csv', 'a') as myfile:
            wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
            wr.writerow([totalscore])

        with open('./csv/randomsearchroute.csv', 'r') as myfile:
            best_route = myfile.readlines()[-1]
                    
    return route

