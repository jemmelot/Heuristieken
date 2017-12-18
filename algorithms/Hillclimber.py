#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import os
import sys
import inspect
import csv
import numpy as np
import math
from random import randint
from random import random
from Random_search_for_hc import random_route
from Scorefromroute import scorefromroute
from createnetwerk import createNetwerk
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
sys.path.append('../functions/')
sys.path.append('../classes/')


def hillclimber(main_array, stations, connections, trainamount, max_evaluations):
    """Uses hillclimber algorithm."""

    def move_operator(initial_route):
        """This function handles the changes to be made to the routes."""

        route = initial_route.copy()

        # generate two random indices
        i = np.random.choice(len(route))
        j = randint(2, len(route[i]) - 1)

        # find and replace a random station
        new_route = []
        index = stations.index(route[i][j - 1])
        nonzero_count = np.count_nonzero(main_array[index, :] > 0)
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
        total_time = 0

        # if the number equals zero, fill in the new route forwards
        if rnd == 0:
            # insert new station at given random position
            route[i][j] = stations[index_new]

            # up to the replaced station, the new route stays the same
            new_route = [0]
            for k in range(1, j):
                new_route.append(route[i][k])

            # re-calculate travel time
            for l in range(1, j - 1):
                index1 = stations.index(new_route[l])
                index2 = stations.index(new_route[l + 1])
                total_time += main_array[index1, index2]

        # else, fill in backwards
        if rnd == 1:
            # insert new station at given random position
            route[i][j] = stations[index_new]

            # up to the replaced station, the new route stays the same
            new_route = []
            for k in range(j - 1, len(route[i]) - 1):
                new_route.append(route[i][k])
            new_route.reverse()
            new_route.insert(0, 0)

            # re-calculate travel time
            for l in range(1, len(new_route) - 2):
                index1 = stations.index(new_route[l])
                index2 = stations.index(new_route[l + 1])
                total_time += main_array[index1, index2]

        # fill the rest of the new route at random
        route[i] = new_route
        starting_station = stations.index(route[i][len(new_route) - 1])

        def fillroute(startingstation, totaltime):
            """Uses random search and changed station as starting point to complete the new route."""

            x = np.where(main_array[startingstation, :] > 0)
            r = np.random.choice(x[0])

            if (totaltime + main_array[startingstation][r]) > 120:
                route[i][0] = totaltime

            else:
                route[i].append(stations[r])
                totaltime += main_array[startingstation][r]
                fillroute(r, totaltime)

        fillroute(starting_station, total_time)
        final_route = route.copy()
        return final_route

    def probability(prev_score, next_score, temperature):
        """Determines the probability that the program will pick a worse solution."""

        if next_score > prev_score:
            return 1.0
        else:
            return math.exp(-abs(next_score - prev_score) / temperature)

    def anneal(solution):
        """Uses simulated annealing to avoid local maxima."""

        # calculate score of the randomly generated routes and arbitrarily set the temperature
        current_score = 0
        T = 1.0
        alpha = 0.9  # the optimal value for apha has been approached by trial and error
        num_evaluations = 0
        annealing_iterations = 3
        while max_evaluations > num_evaluations:
            i = 1
            while i <= annealing_iterations:
                current_solution = solution.copy()
                current_score = float(scorefromroute(current_solution, connections, trainamount))

                # calculate new solution and determine the score and probability
                new_route = move_operator(current_solution)
                new_score = float(scorefromroute(new_route, connections, trainamount))

                # determine whether or not the new score should be saved based on simulated annealing
                prob = probability(current_score, new_score, T)
                if prob > random():
                    solution = new_route.copy()
                    current_score = new_score
                i += 1
            # reduce the temperature with every iteration
            T = T * alpha
            num_evaluations += 1

            # after every 1000 simulated annealing iterations, write the score to csv
            with open('./csv/hc_scores.csv', 'a') as myfile:
                wr = csv.writer(myfile, sys.stdout, lineterminator='\n')
                wr.writerow([current_score])
            print(num_evaluations, current_score)

    rng_route = random_route(main_array, stations, trainamount)
    anneal(rng_route)
    return solution, current_score
