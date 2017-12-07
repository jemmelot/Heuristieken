#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import random
import sys
sys.path.append('../classes/')
from ScoreVariables import score_variables
#from Score       import Score
#from Graph       import Graph
#import matplotlib.pyplot as plt

# list of all stations
stations = []
connections = []
critical = []
criticalconnections = []

# list of coordinates
latitude = []
longitude = []

# import data from Stations csv file
with open('../csv/StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        stations.append(row[0])
        latitude.append(row[1])
        longitude.append(row[2])
        # create list of critical stations
        if "Kritiek" in row:
            critical.append(row[0])


# import data from Connections csv file
with open('../csv/ConnectiesHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        connections.append(row)

connectiontimes = [int(connection[2]) for connection in connections]


# Scorefunctie: S = p*10000 - (t*20 + m/10000)
# p het percentage van de bereden kritieke verbindingen
# t het aantal treinen
# m het totaal door alle treinen samen gereden aantal minuten in de lijnvoering.
max_s = 10000.000
max_t = -(7 * 20)
max_m = -(120)
max_p = max_s + max_t + max_m


# instantiate numpy array
array = np.zeros((22, 22))

# fill in numpy array accordingly
for station in stations:
    for connection in connections:
        if connection[0] == station:
            for item in critical:
                if connection[0] in critical:
                    if connection not in criticalconnections:
                        criticalconnections.append(connection)
            row = stations.index(station)
            column = stations.index(connection[1])
            array[row][column] = connection[2]
        if connection[1] == station:
            if connection[1] in critical:
                if connection not in criticalconnections:
                    criticalconnections.append(connection)
            row = stations.index(station)
            column = stations.index(connection[0])
            array[row][column] = connection[2]


# calculate added value for station being critical
val_critic = max_p / len(criticalconnections)

# calculate added value for duration of connection
# ECHTE VERSIE val_time = [float(x / 10000) for x in connectiontimes]
val_time = [float(-x) for x in connectiontimes]

# give a value to each connection
for connection in connections:
    if connection[0] in critical or connection[1] in critical:
        connection.append(val_critic)
    else:
        connection.append(0)
    connection.append(x)
    for i in val_time:
        if connection[4] == x:
            connection[4] = i
    connection.append(int(connection[3]) + connection[4])


print(connections)
print(val_time)

# start greedy algorithm
numbertracks = 7


# get random starting stations
trackstart = []
max_lenght = 120

for i in range(numbertracks):
    trackstart.append(random.randrange(0, 28))
print(trackstart)

routes = [[] for i in range(numbertracks)]

# set starting stations in routes
counter = 0
for track in trackstart:
    routes[counter] = connections[track][0]
    counter += 1

counter = 0
for i in range(numbertracks):
    scorelist = []
    for connection in connections:
        if routes[counter] == connection[0]:
            print(connection[0])
            scorelist.append(connection[5])
            print(scorelist)
    counter += 1

print routes







