#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import sys
sys.path.append('./classes/')
sys.path.append('./functions/')
sys.path.append('./algorithms/')
#from ScoreVariables import score_variables
from Score import score
from Visualization  import visualization
from Random_search	import random_route
from Hillclimber    import hillclimber
import matplotlib.pyplot as plt

# list of all stations
stations = []
connections = []
critical_stations = []

# list of coordinates
longitude = []
latitude = []

# read stations from csv file
with open('./csv/StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        stations.append(row[0])

# read connections from csv file
with open('./csv/ConnectiesHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        connections.append(row)

# read latitude from csv file
with open('./csv/StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        latitude.append(row[1])

# read longitude from csv file
with open('./csv/StationsHolland.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        longitude.append(float(row[2]))

# read critical stations from csv file
with open('./csv/StationsHolland.csv', 'r') as csvfile:
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


evaluations = 10000

'''
# random search 
i = 1
while i < evaluations:
    visited_connections, route = random_route(main_array, starting_stations, stations)
    random_score = score(visited_connections, route)
    #csvwrite(random_score)
    i += 1
'''

# breadth first
# TODO

# hill-climber
hc_score = hillclimber(evaluations)

# greedy
# TODO

<<<<<<< HEAD
for row in route:
    print(row)	

object = score_variables()

# score function parameters
p	= object.p(main_array, visited_connections, stations, critical_stations)
t   = object.t(visited_connections)
min = object.min(route)

final_score = score(p, t, min)

print(p)
print(final_score)
print(latitude)
# print the highest score for every algorithm
#print("Random search:", random_score)
#print("Breadth-first:", bf_score)
#print("Hillclimber:", hc_score)
#print("Greedy:", greedy_score)


# create and print visualization
visualization(longitude, latitude, stations, route, critical_stations, main_array, final_score)

