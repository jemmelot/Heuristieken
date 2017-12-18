import numpy as np
import csv
from ScoreIntegrated import score_integrated

def breadth_first_route(main_array, stations, critical_stations, trains, iterations):
'''
This function determines a certain number of routes, each starting at a random station.
The route are determined through a breadth first method. 

args: 
- numpy array containing all connections and travel times
- list containing all stations
- list containing all critical stations
- amount of routes to calculate
- amount of iterations (different sets of random starting stations)

type: function

returns: best scoring set of routes after all iterations, also the score itself
'''	
	# store the 'tree' of every station in a list
	explored = [[] for i in range(len(stations))]

	'''
	For each starting station, determine their 'tree'. A tree contains the way all stations connect,
	starting at a certain station
	'''	
	# fill in the every tree
	for i in range(len(stations)):
		starting_station = stations[i]
				
		# initiate queue
		queue = [starting_station]
		
		# initiate list of unique visited stations
		visited = [starting_station]
		
		# expand tree until it contains all stations
		while queue:
			# add stations to the tree
			node = queue.pop(0)
			explored[i].append(node)
					
			# check numpy array at the row of the current station to find all connected stations
			all_stations = main_array[stations.index(node)]
			all_neighbours = np.nonzero(all_stations)
			neighbour_values = all_neighbours[0]
			neighbour_values = neighbour_values.tolist()
			for row in neighbour_values:
				if stations[int(row)] in visited:
					neighbour_values.remove(row)
			neighbour_values = (all_stations[neighbour_values])
												
			neighbours = all_neighbours[0]
							
			# check which connected stations haven't been visited before and add all to the queue
			for neighbour in neighbours:
				if stations[neighbour] not in visited:						
					queue.append(stations[neighbour])
					visited.append(stations[neighbour])
		
	def bfs_paths(graph, start, goal, available):
		'''
		Make a list containing all possible routes between a random starting station and reachable end station
		'''
		queue = [(start, [start])]
		while queue:
			connection_set = set()
			(vertex, path) = queue.pop(0)
			test = np.nonzero(graph[stations.index(vertex)])[0]
			for connection in test:
				if stations[connection] in available:
					connection_set.add(stations[connection])
						
			for next in connection_set - set(path):
				if next == goal:
					yield path + [next]
				else:
					queue.append((next, path + [next]))	
	
	# for every starting station, determine all possible ways to traverse their trees
	reach = [[] for i in range(len(stations))]	
	for i in range(len(stations)):
		row = explored[i]
		reach[i] = list(bfs_paths(main_array, row[0], row[len(row) - 1], row))
			
	# variable for all time highest score and route
	all_time_highest_score = 0
	all_time_highest_route = [[] for i in range(trains)]
		
	with open("holland.csv", 'a', newline='') as f:
		writer = csv.writer(f)
		# calculate the best score from a set of random starting stations 100 times
		try:
			for i in range(iterations):
				'''
				Make a list of random starting stations. Iterate over every option to traverse the tree of a station. 
				First, determine the best scoring route for	just the first starting station. The second route will have its
				score combined with that of the first. The third will have its score combined with the first and second, and so on.
				This way every next best route will be determined based on how it fits in with the already made routes.
				'''
				# matrix to track how many times each station has been visited
				visited_connections = np.zeros((len(stations), len(stations)))
						
				# make a list of random starting stations		
				indexes = list(np.random.choice(range(len(stations)), trains, replace=False))
													
				# keep track of best scoring routes
				highest_score = 0.0
				highest_p = 0
				highest_route = [[] for l in range(trains)]
				
				# make a temporary matrix to copy other arrays into in between loops
				temp = np.zeros((len(stations), len(stations)))
						
				# store routes in one big list
				route = [[] for l in range(trains)]
						
				'''
				first determine best scoring route from the first set of start-end possibilities,
				then take that route into consideration at the next route etc.
				'''
				for m in range(trains):
					# check all possibilities between two stations
					for possibility in reach[indexes[m]]:
						# clear currect route for every possibility
						route[m].clear()
						
						# variables to track the total travel time of a route
						total_time = 0
						time = 0
						
						visited_connections = temp.copy()
						
						'''
						For every option from a starting station, cut it to a maximum of 120 (or 180) minutes 
						'''
						for station in possibility:						
							if possibility.index(station) == 0:
								route[m].append(station)
							
							else:
								# determine the travel time between two stations
								time = int(main_array[stations.index(possibility[possibility.index(station) - 1])][stations.index(station)])
								
								if (total_time + time) > 120:
									break
								
								# if allowed by time, add station and its travel time to a route
								else:
									route[m].append(station)
									visited_connections[stations.index(possibility[possibility.index(station) - 1])][stations.index(station)] += 1
									visited_connections[stations.index(station)][stations.index(possibility[possibility.index(station) - 1])] += 1
									total_time += time
						
						route[m].insert(0, total_time)
						
						'''
						Calculate the score for the current combination of routes. For this algorithm, the score is calculated
						using a different score function than the greedy and hill climber algorithms. This is because this algorithm uses a matrix
						comparison between the main matrix and the matrix containing visited stations/connnections of a set of routes to determine 
						the percentage of critical stations, whereas the others use modified versions of the list containing all direct connections.
						Both methods of calculating the score work as intented and produce the same output.
						'''
						final_score = float(score_integrated(main_array, visited_connections, stations, route, critical_stations,(m+1)))
						
						# if a combination of routes gets a new highest score, set it as the current best scoring combination for following iterations
						if final_score > highest_score:
							highest_score = final_score
							highest_route[m] = route[m].copy()
							highest_visited = visited_connections.copy()
																
					temp = highest_visited.copy()
					route = highest_route.copy()
				
				# if the best scoring combination of routes from a certain set of starting stations gets a new highest score, save it as the current all time highest for following iterations
				if highest_score > all_time_highest_score:
					all_time_highest_score = highest_score
					for a in range(trains):
						all_time_highest_route[a] = highest_route[a].copy()
					all_time_highest_visited = highest_visited.copy()
				
				# after every set of starting stations, write the current all time highest score to a csv file to plot the curve.
				writer.writerow([round(all_time_highest_score, 5)])	
		
		# if the algorithm is interrupted before all iterations are done, signify it and proceed to print current all time best scoring set of routes
		except KeyboardInterrupt:
			print("INTERRUPTED")
					
	return all_time_highest_route, all_time_highest_score
