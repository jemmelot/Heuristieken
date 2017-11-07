#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import csv

# list of all stations
stations = []
connections = []

# matrix to store all station information into
Width, Height = 22, 22;
matrix = [[0 for x in range(Width)] for y in range(Height)]

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

# fill in matrix accordingly		
for station in stations:
	for connection in connections:
		if connection[0] == station: 
			row = stations.index(station)
			column = stations.index(connection[1])
			matrix[row][column] = connection[2]
		if connection[1] == station:
			row = stations.index(station)
			column = stations.index(connection[0])
			matrix[row][column] = connection[2]

# print matrix
for i in range(len(matrix)):
	print(matrix[i])

# show all possible direct connection and their time			
for i in range(len(matrix)):	
	for j in range(len(matrix)):
		if matrix[i][j] != 0:
			print(stations[i] + ' ' + stations[j] + ' = ' + matrix[i][j])
	