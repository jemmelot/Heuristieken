#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np

class score_variables():
    """Implements critical connections and the corresponding travel time."""

    def p(self, main_array, visited_connections, stations, critical_stations):
        """Determines what percentage of critical connections are hit"""

        if len(critical_stations) != len(stations):
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
			
        else:
            all_criticals = 0
            missed_criticals = 0

            for i in range(len(visited_connections)):
                x = np.count_nonzero(main_array[i, :] > 0)
                all_criticals += x

                y = np.count_nonzero(visited_connections[i, :] > 0)
                if not x == y:
                    missed_criticals += (x - y)
				
            p = ((all_criticals - missed_criticals)/all_criticals)	
		        
        return p, (all_criticals - missed_criticals)
    
    def min(self, initial_array, trains):
        """Calculates the total travel time of every route combined."""

        time = 0

        for i in range(trains):
            time += initial_array[i][0]

        return time