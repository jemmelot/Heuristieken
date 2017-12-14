#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
import numpy as np
import math
from random import randint
from random import random
from RailNL import main_array, starting_stations, stations, critical_stations
from Random_search import random_route
sys.path.append('../functions/')
from Score import score

def hillclimber(max_evaluations):
    """Uses hillclimber algorithm."""
    def move_operator(route):
        """This function handles the changes to be made to the routes."""

        # generate two random indices
        i = np.random.choice(len(route))
        j = randint(2, len(route[i]) - 1)

        # find and replace a random station
        new_route = []
        index = stations.index(route[i][j - 1])
        nonzero_count   = np.count_nonzero(main_array[index, :] > 0)
        nonzero_indices = np.where(main_array[index, :] > 0)[0]

        # make sure a different station is chosen, if possible
        index_old = stations.index(route[i][j])
        index_new = index_old
        if nonzero_count > 1:
            while index_old == index_new:
                rng = np.random.choice(nonzero_count)
                index_new = nonzero_indices[rng]
        else:
            index_new = nonzero_indices[0]

        # generate random number (either 0 or 1)
        rnd = np.random.choice(2)

        # if the number equals zero, fill in the new route forwards
        if rnd == 0:
            # subtract visited connections of the to be deleted stations
            for n in range(j, len(route[i]) - 2):
                index1 = stations.index(route[i][n])
                index2 = stations.index(route[i][n + 1])
                visited_connections[index1][index2] -= 1
                visited_connections[index2][index1] -= 1

            # insert new station at given random position
            route[i][j] = stations[index_new]

            # up to the replaced station, the new route stays the same
            new_route = [0]
            for k in range(1, j):
                new_route.append(route[i][k])

            # re-calculate travel time
            total_time = 0
            for l in range(1, j - 1):
                index1 = stations.index(new_route[l])
                index2 = stations.index(new_route[l + 1])
                total_time += main_array[index1, index2]

        # else, fill in backwards
        else:
            # subtract visited connections of the to be deleted stations
            for n in range(1, j - 1):
                index1 = stations.index(route[i][n])
                index2 = stations.index(route[i][n + 1])
                visited_connections[index1][index2] -= 1
                visited_connections[index2][index1] -= 1

            # insert new station at given random position
            route[i][j] = stations[index_new]

            # up to the replaced station, the new route stays the same
            new_route = []
            for k in range(j - 1, len(route[i]) - 1):
                new_route.append(route[i][k])
            new_route.reverse()
            new_route.insert(0, 0)

            # re-calculate travel time
            total_time = 0
            for l in range(1, len(new_route) - 2):
                index1 = stations.index(new_route[l])
                index2 = stations.index(new_route[l + 1])
                total_time += main_array[index1, index2]

        # fill the rest of the new route at random
        route[i] = new_route
        starting_station = stations.index(route[i][len(new_route) - 1])
        def fillroute(starting_station, total_time):
            """Uses random search and changed station as starting point to complete the new route."""

            x = np.where(main_array[starting_station, :] > 0)
            r = np.random.choice(x[0])

            if (total_time + main_array[starting_station][r]) > 120:
                route[i][0] = total_time

            else:
                route[i].append(stations[r])
                total_time += main_array[starting_station][r]
                visited_connections[starting_station][r] += 1
                visited_connections[r][starting_station] += 1
                fillroute(r, total_time)


        fillroute(starting_station, total_time)
        return route, visited_connections


    def probability(prev_score, next_score, temperature):
        """Determines the probability that the program will pick a worse solution."""

        if next_score > prev_score:
            return 1.0
        else:
            return math.exp(-abs(next_score - prev_score) / temperature)


    def anneal(solution, connections):
        """Uses simulated annealing to avoid local maxima."""

        # calculate score of the randomly generated routes and arbitrarily set the temperature
        current_score = score(connections, solution)
        T = 1.0
        alpha = 0.995
        num_evaluations = 0
        #annealing_iterations = 50
        while max_evaluations > num_evaluations:
            #i = 1
            #while i <= annealing_iterations:
                # calculate new solution and determine the score and probability
            new_solution, new_connections = move_operator(solution)
            new_score = score(new_connections, new_solution)
            prob = probability(current_score, new_score, T)
            if prob > random():
                solution = new_solution
                current_score = new_score
                #i += 1
            T = T * alpha
            num_evaluations += 1
            #csvwrite(current_score)
            print(num_evaluations, current_score)
        return solution, current_score

    visited_connections, route = random_route(main_array, starting_stations, stations)
    solution, current_score = anneal(route, visited_connections)

    return current_score
