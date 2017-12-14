#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
from Lijnvoering 	import Lijnvoering
from Score       	import score
from Graph       	import graph
from Random_search	import random_route
from Breadth_first	import breadth_first_route
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

# instantiate numpy array to store all connections and travel times
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
Below are the function calls to the different algorithms
'''
# random search 
#visited_connections, route = random_route(main_array, starting_stations, stations)

# breadth first
visited_connections, route, final_score = breadth_first_route(main_array, starting_stations, stations, critical_stations)
#breadth_first_route(main_array, starting_stations, stations, critical_stations)
#print(explored)

# hill-climber
# TODO

# greedy
# TODO
'''
for row in route:
    print(row)	

object = Lijnvoering()

# score function parameters
p	= object.p(main_array, visited_connections, stations, critical_stations)
t   = object.t(visited_connections)
min = object.min(route)

final_score = score(p, t, min)

print(p)
print(final_score)
'''
# create and print graph
graph(longitude, latitude, stations, route, critical_stations, main_array, final_score)
