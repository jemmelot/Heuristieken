#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
sys.path.append('../classes/')
from createnetwerk import createNetwerk

def random_route(trains_amount):
	"""Calculates routes at random."""

	# the seven calculated routes will be stored in this variable
	route = [[] for i in range(trains_amount)]
	
	# instantiate numpy array to keep track of how often every station is visited
	visited_connections = np.zeros((22, 22))
	
	# create seven random routes
	for i in range(trains_amount):
		total_time = 0
		
		rnd = np.random.choice(starting_stations)
		starting_station = stations.index(rnd)
		route[i].append(stations[starting_station])
		
		def routes(starting_station, total_time):
			x = np.where(array[starting_station, :] > 0)
			r = np.random.choice(x[0])

			if (total_time + array[starting_station][r]) > 120:
				route[i].insert(0, total_time)
								
			else:
				route[i].append(stations[r])
				total_time += array[starting_station][r]
				visited_connections[starting_station][r] += 1
				visited_connections[r][starting_station] += 1
				routes(r, total_time)

		routes(starting_station, total_time)

	return visited_connections, route
