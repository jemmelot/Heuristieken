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
#print array
print(array)

# show all possible direct connection and their time			
for i in range(len(array)):	
	for j in range(len(array)):
		if array[i][j] != 0:
			print(stations[i] + ' ' + stations[j] + ' = ',end='')
			print(int(array[i][j]))
'''

# instantiate numpy array
visited_connections = np.zeros((22, 22))

# breadth first algorithm, early version
# show possible stations from a starting station within 120 minutes
def breadth_first(main_array, stations):
	# the seven calculated routes will be stored in this variable
	explored = [[] for i in range(7)]

	for i in range(7):		
		total_time = 0
		
		starting_station = np.random.choice(stations)
				
		# initiate queue
		queue = [starting_station]
		
		# initiate list of unique visited stations
		visited = [starting_station]
		
		while total_time < 120:
			node = queue.pop(0)
			explored[i].append(node)
					
			# check numpy array at the row of a station to find all connected stations
			all_stations = main_array[stations.index(node)]
			all_neighbours = np.nonzero(all_stations)
			neighbour_values = all_neighbours[0]
			neighbour_values = neighbour_values.tolist()
			for row in neighbour_values:
				if stations[int(row)] in visited:
					neighbour_values.remove(row)
			neighbour_values = (all_stations[neighbour_values])
			#print(max(neighbour_values))
			if len(neighbour_values) > 0:
				total_time += max(neighbour_values)
			#print(total_time)
			
			neighbours = all_neighbours[0]
			#print(neighbour_values)
			
			# check which connected stations haven't been visited before and add all to the queue
			for neighbour in neighbours:
				if stations[neighbour] not in visited:
					#if (total_time + array[stations.index(node)][neighbour]) > 120:
						#break
					queue.append(stations[neighbour])
					visited.append(stations[neighbour])
					#total_time += array[stations.index(node)][neighbour]
						
	return explored

def bfs_paths(graph, start, goal, available):
	queue = [(start, [start])]
	while queue:
		connection_set = set()
		(vertex, path) = queue.pop(0)
		test = np.nonzero(graph[stations.index(vertex)])[0]
		for connection in test:
			if stations[connection] in available:
				connection_set.add(stations[connection])
		
		#print(connection_set)
		for next in connection_set - set(path):
			if next == goal:
				yield path + [next]
			else:
				queue.append((next, path + [next]))	
	
# call algorithm function with the array index of a starting station
ans = breadth_first(main_array, stations)

reach = [[] for i in range(7)]
route = [[] for i in range(7)]
i = 0

for row in ans:
	reach[i] = list(bfs_paths(main_array, row[0], row[len(row) - 1], row))
	i += 1
	
for i in range(7):
	if len(reach[i]) == 1:
		option = 0
	
	else:
		option = np.random.randint(0, (len(reach[i]) - 1))
	
	route[i].append(reach[i][option])

for i in range(7):
	print(route[i])
	total_time = 0
	for station in route[i][0]:
		print(station)
		if route[i][0].index(station) != 0:
			time = main_array[stations.index(route[i][0][route[i][0].index(station) - 1])][stations.index(route[i][0][route[i][0].index(station)])]
			visited_connections[stations.index(route[i][0][route[i][0].index(station) - 1])][stations.index(route[i][0][route[i][0].index(station)])] += 1
			visited_connections[stations.index(route[i][0][route[i][0].index(station)])][stations.index(route[i][0][route[i][0].index(station) - 1])] += 1
			total_time += time
			
	route[i].insert(0, total_time)

print(visited_connections)	
	
for row in route:
	print(row)

