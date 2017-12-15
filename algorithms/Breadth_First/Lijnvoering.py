#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np

class Lijnvoering():
    """Implements critical connections and the corresponding travel time."""

    def p(self, main_array, visited_connections, stations, critical_stations):
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
		
        all_criticals -= 1
		
        p = ((all_criticals - missed_criticals)/20)
		        
        return p, (all_criticals - missed_criticals)


    def t(self, trains_array):
        """Calculates how often mutiple trains pass the same connection."""

        # fetch array displaying total amount of trains per connection,
        # and count how often connections are visited more than once
        array = np.array(trains_array)
        t2 = np.count_nonzero(array == 2)
        t3 = np.count_nonzero(array == 3)
        t4 = np.count_nonzero(array == 4)
        t5 = np.count_nonzero(array == 5)
        t6 = np.count_nonzero(array == 6)
        t7 = np.count_nonzero(array == 7)

        t = t2 * 2 + t3 * 3 + t4 * 4 + t5 * 5 + t6 * 6 + t7 * 7

        return t


    def min(self, initial_array, iterations):
        """Calculates the total travel time of every route combined."""

        time = 0

        for i in range(iterations):
            time += initial_array[i][0]

        return time