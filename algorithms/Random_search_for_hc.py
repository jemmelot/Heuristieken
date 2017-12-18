#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import sys

sys.path.append('../classes/')
from createnetwerk import createNetwerk


def random_route(array, stations, trains_amount):
    """Calculates routes at random."""

    # the seven calculated routes will be stored in this variable
    route = [[] for i in range(trains_amount)]

    # create seven random routes
    for i in range(trains_amount):
        total_time = 0

        rnd = np.random.choice(stations)
        starting_station = stations.index(rnd)
        route[i].append(stations[starting_station])

        def routes(starting_station, total_time):
            x = np.where(array[starting_station, :] > 0)
            r = np.random.choice(x[0])

            if (total_time + array[starting_station][r]) > 120:
                route[i].insert(0, total_time)

            else:
                route[i].append(stations[r])
                total_time += array[starting_station][r]
                routes(r, total_time)

        routes(starting_station, total_time)

    return route