import numpy as np
from Lijnvoering 	import Lijnvoering
from Score       	import score

def breadth_first_route(main_array, starting_stations, stations, critical_stations):
	
	all_time_highest = 0
	
	'''
	for i in range(100):
	'''
	visited_connections = np.zeros((22, 22))

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
				if len(neighbour_values) > 0:
					total_time += max(neighbour_values)
								
				neighbours = all_neighbours[0]
								
				# check which connected stations haven't been visited before and add all to the queue
				for neighbour in neighbours:
					if stations[neighbour] not in visited:						
						queue.append(stations[neighbour])
						visited.append(stations[neighbour])
													
		return explored
	
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
		
	# call algorithm function with the array index of a starting station
	ans = breadth_first(main_array, stations)

	# put all 7 lists (each containing all possible start-end routes) in one big list
	reach = [[] for i in range(7)]
	i = 0

	for row in ans:
		reach[i] = list(bfs_paths(main_array, row[0], row[len(row) - 1], row))
		i += 1
	
	# keep track of best scoring sets (of 7 routes) 
	highest_score = 0
	highest_p = 0
	highest_route = []
	
	'''
	for attempts in range(1000):
	'''
	route = [[] for i in range(7)]
	
	print(reach[0])
	
	# determine best scoring route from the first set of start-end possibilities
	for possibility in reach[0]:
		route[0] = []
		route[0].append(possibility)
		total_time = 0
		
		for station in route[0][0]:
			if route[0][0].index(station) != 0:
				time = main_array[stations.index(route[0][0][route[0][0].index(station) - 1])][stations.index(route[0][0][route[0][0].index(station)])]
				visited_connections[stations.index(route[0][0][route[0][0].index(station) - 1])][stations.index(route[0][0][route[0][0].index(station)])] += 1
				visited_connections[stations.index(route[0][0][route[0][0].index(station)])][stations.index(route[0][0][route[0][0].index(station) - 1])] += 1
				total_time += time
				
		route[0].insert(0, total_time)
		
		object = Lijnvoering()

		# score function parameters
		p	= object.p(main_array, visited_connections, stations, critical_stations)
		t   = 7
		min = object.min(route, 1)

		final_score = score(p, t, min)
		
		print(route)		
		print(p)
		print(final_score)
		
		if final_score > highest_score:
			highest_p = p
			highest_score = final_score
			highest_route = route
	
	print(highest_route)
	print(highest_p)
	print(highest_score)
	
	'''
	for i in range(7):
		# for the first set of start-end possibilities, pick the one with the best score
		if len(reach[i]) == 1:
			option = 0
		
		else:
			option = np.random.randint(0, (len(reach[i]) - 1))
		
		route[i].append(reach[i][option])
	
		total_time = 0
		
		for station in route[i][0]:
			if route[i][0].index(station) != 0:
				time = main_array[stations.index(route[i][0][route[i][0].index(station) - 1])][stations.index(route[i][0][route[i][0].index(station)])]
				visited_connections[stations.index(route[i][0][route[i][0].index(station) - 1])][stations.index(route[i][0][route[i][0].index(station)])] += 1
				visited_connections[stations.index(route[i][0][route[i][0].index(station)])][stations.index(route[i][0][route[i][0].index(station) - 1])] += 1
				total_time += time
				
		route[i].insert(0, total_time)
		
	object = Lijnvoering()

	# score function parameters
	p	= object.p(main_array, visited_connections, stations, critical_stations)
	t   = 7 #object.t(visited_connections)
	min = object.min(route)

	final_score = score(p, t, min)
			
	if final_score > highest_score:
		highest_p = p
		highest_score = final_score
		highest_route = route
			
	if highest_score > all_time_highest:
		all_time_highest = highest_score
		all_time_highest_score = highest_score
		all_time_highest_route = highest_route
		print(all_time_highest)
	
	for row in all_time_highest_route:
		print(row)
	
	return visited_connections, route
	'''	