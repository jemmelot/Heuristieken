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

class score_from_route():

    def __init__(self, route, connections, trainamount):
        self.route = route
        self.connections = connections
        self.trainamount = trainamount
        self.t = self.t()
        self.min = self.min()
        self.p = self.p()
        self.totalscore = self.totalscore(self.p, self.t, self.min)

    def __str__(self):
        return str(float(self.totalscore))

    def t(self):
        t = self.trainamount
        return t

    def min(self):
        min = max([row[0] for row in self.route])
        return min
            
    def p(self):
        routecriticalconnections = 0
        connectioncheck1 = []
        rowcounter = 0
        counter = 0
        for i in range(self.trainamount):
            for row in self.route[rowcounter:rowcounter+1]:
                connectioncheck1.append([row[1]])
                for i in row[1:len(row)]:
                    i = row.index(i)
                    connectioncheck1.append([row[i]])
                    connectioncheck1[counter].extend([row[i]])
                    counter+=1
            del connectioncheck1[-1]
            rowcounter += 1
        connectioncheck2 = []
        routecriticalconnections = 0
        for check in connectioncheck1:
            totalcriticalconnections = 0
            for connection in self.connections:
                if connection[3] != 0:
                    totalcriticalconnections += 1
                if check[0] in connection and check[1] in connection:
                    if connection[0:2] not in connectioncheck2:
                        if connection[3] != 0:
                            routecriticalconnections += 1
                            connectioncheck2.append(connection[0:2])

        p = routecriticalconnections / totalcriticalconnections
        return p

    def totalscore(self, p, t, min):
        totalscore = (p * 10000) - ((t * 20) + (min/10000))
    
        return totalscore
