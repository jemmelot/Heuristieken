#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
from Lijnvoering import Lijnvoering
from Score       import score
from Graph       import graph
import matplotlib.pyplot as plt

# list of all stations
stations = []
connections = []
critical_stations = []

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

# read critical stations from csv file
with open('StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        # check whether connection is critical
        if "Kritiek" in row:
            critical_stations.append(row[0])

# hardcode an array of every station with only one connection
end_of_the_line = ["Den Helder", "Dordrecht"]

starting_stations = critical_stations + end_of_the_line

# instantiate numpy array
main_array = np.zeros((22, 22))

# fill in numpy array accordingly
for station in stations:
    for connection in connections:
        if connection[0] == station:
            row = stations.index(station)
            column = stations.index(connection[1])
            main_array[row][column] = connection[2]
        if connection[1] == station:
            row = stations.index(station)
            column = stations.index(connection[0])
            main_array[row][column] = connection[2]

'''
#print csv array
print(main_array)

# show all possible direct connection and their time			
for i in range(len(main_array)):	
	for j in range(len(main_array)):
		if main_array[i][j] != 0:
			print(stations[i] + ' ' + stations[j] + ' = ',end='')
			print(int(main_array[i][j]))
'''

# the seven calculated routes will be stored in this variable
route = [[] for i in range(7)]
for row in route:
    print(row)

# instantiate numpy array to keep track of how often every station is visited
visited_connections = np.zeros((22, 22))

# use algorithm
for i in range(7):
    starting_station = np.random.choice(starting_stations)
    if any(i in s for s in stations):
        i = stations.index(i)

    # breadth_first
    route               = breadth-first_route(main_array, starting_station, route)
    visited_connections = breadth-first_t(main_array, starting_station, visited_connections)

    # hill-climber


    # greedy



object = Lijnvoering()

p	= object.p(main_array, visited_connections, stations, critical_stations)
t   = object.t(visited_connections)
min = object.min(route)

final_score = score(p, t, min)

print(percentage)
print(final_score)

# create and print graph
graph(longitude, latitude, stations, route, critical_stations, main_array, final_score)