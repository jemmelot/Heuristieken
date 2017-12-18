#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import sys
sys.path.append('../classes/')
sys.path.append('../functions/')
sys.path.append('../algorithms/')
import matplotlib.pyplot as plt

def histogram(title, csvfile):
    
    results = []
    
    with open(csvfile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            row = "".join(row)
            results.append(row)

    results = list(map(float, results))
    plt.hist(results)
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    title = 'Frequency of result ' + title
    plt.title(title)

    plt.show()
