#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

class Score():
    """Calculates score of results."""

    def __init__(self, critical, trains, commute):
        """Calculates total score."""

        p   = critical
        t = trains
        min = commute

        # arbitrary formula to calculate score
        score = p*10000 - (t*20 + min/100000)

        return score


