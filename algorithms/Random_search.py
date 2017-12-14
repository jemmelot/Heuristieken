import numpy as np

def random_route(main_array, starting_stations, stations):
	# the seven calculated routes will be stored in this variable
	route = [[] for i in range(7)]
	
	# instantiate numpy array to keep track of how often every station is visited
	visited_connections = np.zeros((len(stations), len(stations)))
	
	# create seven random routes
	for i in range(7):
		total_time = 0
		
		starting_station = np.random.choice(starting_stations)
		if any(starting_station in s for s in stations):
			starting_station = stations.index(starting_station)
		
		route[i].append(stations[starting_station])
		
		def routes(starting_station, total_time):
			x = np.where(main_array[starting_station, :] > 0)
			r = np.random.choice(x[0])

			if (total_time + main_array[starting_station][r]) > 120:
				route[i].insert(0, total_time)
								
			else:
				route[i].append(stations[r])
				total_time += main_array[starting_station][r]
				visited_connections[starting_station][r] += 1
				visited_connections[r][starting_station] += 1
				routes(r, total_time)
				
		routes(starting_station, total_time)

	return visited_connections, route	
