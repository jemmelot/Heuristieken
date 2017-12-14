import numpy as np
import csv
from Lijnvoering 	import Lijnvoering
from Score       	import score

def breadth_first_route(main_array, starting_stations, stations, critical_stations):
	# the calculated routes will be stored in this variable
	explored = [[] for i in range(len(stations))]

	# fill in the tree for each station
	for i in range(len(stations)):
		starting_station = stations[i]
				
		# initiate queue
		queue = [starting_station]
		
		# initiate list of unique visited stations
		visited = [starting_station]
		
		# for each starting station, determine the maximum reach within two hours
		while queue:
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
												
			neighbours = all_neighbours[0]
							
			# check which connected stations haven't been visited before and add all to the queue
			for neighbour in neighbours:
				if stations[neighbour] not in visited:						
					queue.append(stations[neighbour])
					visited.append(stations[neighbour])
	
	# make a list containing all possible routes between -
	# a random starting station and reachable end station
	def bfs_paths(graph, start, goal, available):
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
	
	# define amount of routes to be created
	iterations = 7
	
	# variable for all time highest score
	all_time_highest_score = 0
	
	with open("test.csv", 'a', newline='') as f:
		writer = csv.writer(f)
		# calculate the best score from a set of random starting stations 100 times
		for i in range(500):
			# matrix to track how many times each station has been visited
			visited_connections = np.zeros((22, 22))

			# put all 'possibilities' lists (each containing all possible start-end routes) in one big list
			reach = [[] for j in range(iterations)]
			
			start_one = stations.index("Den Helder")
			start_two = stations.index("Dordrecht")
			
			index_start_one = np.random.randint(5)
			index_start_two = np.random.randint(5)
			
			indexes = list(np.random.choice(range(22), 5, replace=False))
					
			indexes.insert(index_start_one, start_one)
			indexes.insert(index_start_two, start_two)
					
			for k in range(iterations):
				row = explored[indexes[k]]
				reach[k] = list(bfs_paths(main_array, row[0], row[len(row) - 1], row))
						
			# keep track of best scoring sets
			highest_score = 0
			highest_p = 0
			highest_route = []
			
			temp = np.zeros((22, 22))
					
			# store routes in one big list
			route = [[] for l in range(iterations)]
					
			# first determine best scoring route from the first set of start-end possibilities
			# then take that route into consideration at the next route etc.
			for m in range(iterations):
				# check all possibilities between two stations
				for possibility in reach[m]:
					# clear currect route for every possibility
					route[m] = []
													
					total_time = 0
					time = 0
					
					visited_connections = temp.copy()
					
					# determine the critical percentage and min amount for a route				
					for station in possibility:
						if (total_time + time) <= 120:
							if possibility.index(station) == 0:
								route[m].append(station)
							
							else:
								time = int(main_array[stations.index(possibility[possibility.index(station) - 1])][stations.index(station)])
														
								route[m].append(station)
								visited_connections[stations.index(possibility[possibility.index(station) - 1])][stations.index(station)] += 1
								visited_connections[stations.index(station)][stations.index(possibility[possibility.index(station) - 1])] += 1
								total_time += time
									
					# insert total time for every possible route at the start 
					route[m].insert(0, total_time)
					
					object = Lijnvoering()

					# score function parameters
					p	= object.p(main_array, visited_connections, stations, critical_stations)
					t   = iterations
					min = object.min(route, (m+1))

					final_score = score(p, t, min)
					
					if final_score > highest_score:
						highest_p = p
						highest_score = final_score
						highest_route = route
						highest_visited = visited_connections.copy()
															
				temp = highest_visited.copy()
			
			if highest_score > all_time_highest_score:
				all_time_highest_score = highest_score
				all_time_highest_p = highest_p
				all_time_highest_route = highest_route
				all_time_highest_visited = highest_visited.copy()
				print(all_time_highest_score)
				
			writer.writerow([int(round((all_time_highest_score - 9859.99), 5)*100000)])	
		
	for row in all_time_highest_route:
		print(row)
	
	print(all_time_highest_p)
	#print(all_time_highest_visited)
		
	return all_time_highest_visited, all_time_highest_route, all_time_highest_score
	
	