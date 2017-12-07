#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import sys
sys.path.append('../classes/')
sys.path.append('../functions/')
sys.path.append('../algorithms/')
from ScoreVariables import score_variables
import matplotlib.pyplot as plt

def visualization(longitude, latitude, stations, route, critical, array, final_score):
    '''Create visualization.'''

    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1, adjustable='box', aspect=0.07)
    plt.axis('off')
    ax1.plot(longitude, latitude, 'ro')
    for station in range(len(stations)):
        ax1.text(longitude[station], latitude[station], ' ' + stations[station], fontsize=10)
    for i in range(len(array)):
        for j in range(len(array)):
            if array[i][j] != 0:
                x1, y1 = [longitude[i], longitude[j]], [latitude[i], latitude[j]]
                ax1.plot(x1, y1, marker = 'o', color='black', linestyle='dotted')
    for row in route:
        x1 = [0,0]
        y1 = [0,0]
        #print(row)
        for i in range(1, len(row)):
            #print(i)
            if i % 2 == 0:
                x1[0] = longitude[stations.index(row[i])]
                y1[0] = latitude[stations.index(row[i])]
            elif i % 2 == 1:
                x1[1] = longitude[stations.index(row[i])]
                y1[1] = latitude[stations.index(row[i])]
            if not 0 in x1:
                if not row[i] in critical:
                    ax1.plot(x1, y1, marker = 'o', color = 'green', linestyle='dashed')
                if row[i] in critical:
                    ax1.plot(x1, y1, marker = 'o', color = 'green')

    ax1.legend(['Score: {0:.0f}'.format(final_score)], loc=2, bbox_to_anchor=(-0.5, 1))
    plt.show()


