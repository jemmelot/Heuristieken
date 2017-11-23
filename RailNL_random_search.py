#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
from Lijnvoering import Lijnvoering
from Score       import Score
from Graph       import Graph
import matplotlib.pyplot as plt

# list of all stations
stations = []
connections = []
critical = []

# list of coordinates
longitude = []
latitude = []

# read stations from csv file
with open('StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        stations.append(row[0])

# read connections from csv file
with open('ConnectiesHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        connections.append(row)

# read latitude from csv file
with open('StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        latitude.append(row[1])

# read longitude from csv file
with open('StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        longitude.append(float(row[2]))

with open('StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # check whether connection is critical
        if "Kritiek" in row:
            critical.append(row[0])

# hardcode an array of every station with only one connection
end_of_the_line = ["Den Helder", "Dordrecht"]

starting_station = critical + end_of_the_line

# instantiate numpy array
array = np.zeros((22, 22))

# fill in numpy array accordingly
for station in stations:
    for connection in connections:
        if connection[0] == station:
            row = stations.index(station)
            column = stations.index(connection[1])
            array[row][column] = connection[2]
        if connection[1] == station:
            row = stations.index(station)
            column = stations.index(connection[0])
            array[row][column] = connection[2]

'''
#print array
print(array)

# show all possible direct connection and their time			
for i in range(len(array)):	
	for j in range(len(array)):
		if array[i][j] != 0:
			print(stations[i] + ' ' + stations[j] + ' = ',end='')
			print(int(array[i][j]))
'''

# the seven calculated routes will be stored in this variable
route = [[] for i in range(7)]

# instantiate numpy array to keep track of how often every station is visited
t = np.zeros((22, 22))

# create seven random routes
for j in range(7):
    total_time = 0
    i = np.random.choice(starting_station)
    if any(i in s for s in stations):
        i = stations.index(i)

    route[j].append(stations[i])

    def routes(i):
        x = np.where(array[i, :] > 0)
        r = np.random.choice(x[0])

        global total_time
        if (total_time + array[i][r]) > 120:
            route[j].insert(0, total_time)

        else:
            route[j].append(stations[r])
            total_time += array[i][r]
            t[i][r] += 1
            t[r][i] += 1
            routes(r)


    routes(i)

for row in route:
    print(row)

all_criticals = 0	
missed_criticals = 0

# compare the t array to the main array to check for missed critical connections
for i in range(len(t)):
	if stations[i] in critical:
		x = np.count_nonzero(array[i, :] > 0)
		all_criticals += x
		y = np.count_nonzero(t[i, :] > 0)
		if not x == y:
			missed_criticals += (x - y)

object = Lijnvoering()
score  = Score()

percentage	= object.critical(all_criticals, missed_criticals)
trains   	= object.trains(t)
commute  	= object.commute(route)

final_score = score.score(percentage, trains, commute)

print(percentage)			
print(final_score)

# create and print graph
graph = Graph()
graph.graph(longitude, latitude, station, stations, route, critical, array, final_score)

