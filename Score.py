#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

def score(p, t, min):
    """Calculates total score."""

    score = p*10000 - (t*20 + min/100000)

    return score