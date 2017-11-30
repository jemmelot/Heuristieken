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

# instantiate numpy array
t = np.zeros((22, 22))

# breadth first algorithm, early version
# show possible stations from a starting station within 120 minutes
def breadth_first(array, start):
	total_time = 0
	
	# keep track of explored stations
	explored = []
	
	# initiate queue
	queue = [stations[start]]
	
	# keep track of the level of the search tree
	levels = {}
	levels[start] = 0
	
	# initiate list of unique visited stations
	visited = [stations[start]]
	
	while queue:
		node = queue.pop(0)
		explored.append(node)
		
		# check numpy array at the row of a station to find all connected stations
		all_stations = array[stations.index(node)]
		all_neighbours = np.nonzero(all_stations)
		neighbours = all_neighbours[0]
		
		# check which connected stations haven't been visited before and add all to the queue
		for neighbour in neighbours:
			if stations[neighbour] not in visited:
				if (total_time + array[stations.index(node)][neighbour]) > 120:
					break
				queue.append(stations[neighbour])
				visited.append(stations[neighbour])
				total_time += array[stations.index(node)][neighbour]
				t[stations.index(node)][neighbour] += 1
				t[neighbour][stations.index(node)] += 1
				
				levels[neighbour] = levels[stations.index(node)] + 1
	
	print(levels)
	
	# insert route time at the start of the route list
	explored.insert(0, total_time)
	return explored

# call algorithm function with the array index of a starting station
ans = breadth_first(array, 10)	
print(ans)