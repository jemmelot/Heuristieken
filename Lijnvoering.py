#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
from RailNL.py import initial_array, trains_array

class Lijnvoering():
    """Implements critical connections and the corresponding travel time."""

    def __init__(self):
        """Initialize class Lijnvoering."""

        # initialize an array to be filled with every critical station
        critical = []
        with open('StationsHolland.csv', 'r') as lines:
            for line in lines:
                # check whether connection is critical
                if "Kritiek" in line:
                    critical.append(line)

        self.critical = critical

        # hardcode an array of every station with only one connection
        end_of_the_line = []
        self.endoftheline = end_of_the_line

    def trains(self):
        """Calculate how often mutiple trains pass the same connection."""

        # fetch array displaying total amount of trains per connection,
        # and count how many indices are greater than 1
        array = np.array(trains_array)
        amount = np.count_nonzero(array > 1)

        return amount

    def commute(self):
        """Calculates the total travel time of each route."""

        #initialize travel time
        time = 0

        #TODO

        return time

