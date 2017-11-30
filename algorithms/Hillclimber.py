#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
from RailNL import main_array, starting_stations, stations
from Random_search import random_search
from Score import score

def hillclimber(max_evaluations):
    """Uses the hill climber algorithm."""

    # load 7 random generated routes, stored in route
    visited_connections, route = random_route(main_array, starting_stations, stations)

    # instantiate best set of routes
    best = route
    previous_best_score = score(best) # TODO: aanroepen scorefunctie
    num_evaluations = 1

    def move_operator(route):
        """This function handles the changes to be made to the routes."""

        # pick a random station within a random route
        i = np.random.choice(len(route)) - 1
        j = np.random.choice(len(route[i])) - 1

        # find index of random station in station array and look in the corresponding row in main_array,
        # then count the nonzero values and pick a new value at random
        index = stations.index(route[i][j - 1])
        index_new = index
        x = np.count_nonzero(main_array[index, :] > 0)

        # if there are multiple nonzero values in the given list, make sure the function returns a different index
        if x > 1:
            while index == index_new:
                rng = np.random.choice(x)
                index_new = main_array[index, :].index(rng)

        # insert new station at selected spot
        route[i][j] = stations[index_new]

        # from j onward, refill the list randomly until the travel time limit is reached
        new_route = []
        for k in range(0, j):
            new_route.append(route[i][k])

        # re-calculate total time and visited connections
        total_time = 0
        visited_connections = 0
        for l in range(1, j):
            index1 = stations.index(new_route[l - 1])
            index2 = stations.index(new_route[l])

            total_time += main_array(index1, index2)
            visited_connections += 1

        starting_station = new_route[j]
        return new_route + fillroute(starting_station, total_time), visited_connections


    # fills in an incomplete route, works like random_search
    def fillroute(starting_station, total_time):
        x = np.where(main_array[starting_station, :] > 0)
        r = np.random.choice(x[0])

        if (total_time + main_array[starting_station][r]) > 120:
            new_route.insert(0, total_time)

        else:
            new_route.append(stations[r])
            total_time += main_array[starting_station][r]
            visited_connections[starting_station][r] += 1
            visited_connections[r][starting_station] += 1
            fillroute(r, total_time)


    # analyze result changed route
    while num_evaluations < max_evaluations:
        move_made = False
        for next in move_operator(best):
            if num_evaluations >= max_evaluations:
                break

            # see if this move is better than the current
            next_score = score(next)
            num_evaluations += 1
            if next_score > previous_best_score:
                best = next
                new_best_score = next_score
                move_made = True
                break

        # TODO: simulated annealing
        difference = new_best_score - previous_best_score
        if difference < 0 or e^(-difference/num_evaluations) > random(0,1):
            previous_best_score = new_best_score

        # if no moves are made, there must be a local maximum
        if not move_made:
            break

    return (num_evaluations, new_best_score, best)
