#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
#from RailNL import main_array, starting_stations, stations, critical_stations

def score(visited_connections, route):
    """Calculates total score."""
    
    def p(main_array, visited_connections, stations, critical_stations):
        """Determines what percentage of critical connections are hit"""
    
        all_criticals = 0
        missed_criticals = 0
    
        # compare the t array to the main array to check for missed critical connections
        for i in range(len(visited_connections)):
            if stations[i] in critical_stations:
                x = np.count_nonzero(main_array[i, :] > 0)
            all_criticals += x
            y = np.count_nonzero(visited_connections[i, :] > 0)
            if not x == y:
                missed_criticals += (x - y)
    
        p = ((all_criticals - missed_criticals)/all_criticals)
    
        return p
    
    
    def t(route):
        """Calculates how often mutiple trains pass the same connection."""
    
        # fetch array displaying total amount of trains per connection,
        # and count how often connections are visited more than once
        #array = np.array(visited_connections)
        #t2 = np.count_nonzero(array == 2)
        #t3 = np.count_nonzero(array == 3)
        #t4 = np.count_nonzero(array == 4)
        #t5 = np.count_nonzero(array == 5)
        #t6 = np.count_nonzero(array == 6)
        #t7 = np.count_nonzero(array == 7)
        #t = t2 * 2 + t3 * 3 + t4 * 4 + t5 * 5 + t6 * 6 + t7 * 7
    
        t = len(route)

        return t
    
    
    def min(route):
        """Calculates the total travel time of every route combined."""
    
        time = 0
    
        for i in range(7):
            time += route[i][0]
    
        return time


    percentage = p(main_array, visited_connections, stations, critical_stations)
    trains     = t(route)
    minutes    = min(route)

    score = percentage*10000 - (trains*20 + minutes/100000)
    return score
