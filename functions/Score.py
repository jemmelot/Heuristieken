#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
from createnetwerk import createNetwerk

def score(visited_connections, route):
    """Calculates total score."""

    # initialize network
    x = createNetwork()
    x.loadData()
    x.createMatrix()
    
    def p(visited_connections):
        """Determines what percentage of critical connections are hit"""
    
        all_criticals = 0
        missed_criticals = 0
    
        # compare the t array to the main array to check for missed critical connections
        for i in range(len(visited_connections)):
            if x.stations[i] in x.critical:
                station_count = np.count_nonzero(x.array[i, :] > 0)
            all_criticals += station_count
            connection_count = np.count_nonzero(visited_connections[i, :] > 0)
            if not zero_count == connection_count:
                missed_criticals += (station_count - connection_count)
    
        p = ((all_criticals - missed_criticals)/all_criticals)
    
        return p
    
    
    def t(route):
        """Calculates how often mutiple trains pass the same connection."""

        t = len(route)

        return t
    
    
    def min(route):
        """Calculates the total travel time of every route combined."""
    
        time = 0
        for i in range(len(route)):
            time += route[i][0]
    
        return time


    percentage = p(visited_connections)
    trains     = t(route)
    minutes    = min(route)

    score = percentage*10000 - (trains*20 + minutes/100000)
    return score
