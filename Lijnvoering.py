#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np

class Lijnvoering():
    """Implements critical connections and the corresponding travel time."""

    def critical(self, all_criticals, missed_criticals):
        """Determines what percentage of connections are critical"""

		# calculate percentage of hit critical connections
        percentage = ((all_criticals - missed_criticals)/all_criticals)

        return percentage


    def trains(self, trains_array):
        """Calculates how often mutiple trains pass the same connection."""

        # fetch array displaying total amount of trains per connection,
        # and count how often connections are visited more than once
        array = np.array(trains_array)
        amount2 = np.count_nonzero(array == 2)
        amount3 = np.count_nonzero(array == 3)
        amount4 = np.count_nonzero(array == 4)
        amount5 = np.count_nonzero(array >  4)

        amount = amount2 * 1 + amount3 * 2 + amount4 * 3 + amount5 * 5

        return amount


    def commute(self, initial_array):
        """Calculates the total travel time of each route."""

        # initialize travel time
        time = 0

        # calculate total travel time of all 7 routes
        for i in range(7):
            time += initial_array[i][0]

        return time