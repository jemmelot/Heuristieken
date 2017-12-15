
import numpy as np
import csv
#from Lijnvoering import Lijnvoering
from Score           import score

def breadth_first_route(main_array, starting_stations, stations, critical_stations):
#    object = Lijnvoering()

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

    # for every starting station, determine all possible ways to traverse their trees
    reach = [[] for i in range(len(stations))]
    for i in range(len(stations)):
        row = explored[i]
        reach[i] = list(bfs_paths(main_array, row[0], row[len(row) - 1], row))

    # define amount of routes to be created
    iterations = 7
        
    # variable for all time highest score
    all_time_highest_score = 0
    all_time_highest_route = [[] for i in range(iterations)]

    with open("test.csv", 'a') as f:
        writer = csv.writer(f)
        # calculate the best score from a set of random starting stations 100 times
        for i in range(500):
            # matrix to track how many times each station has been visited
            visited_connections = np.zeros((22, 22))
            
            start_one = stations.index("Den Helder")
            start_two = stations.index("Dordrecht")
            
            index_start_one = np.random.randint(5)
            index_start_two = np.random.randint(5)
            
            indexes = list(np.random.choice(range(22), (iterations - 2), replace=False))
            
            indexes.insert(index_start_one, start_one)
            indexes.insert(index_start_two, start_two)
            
            # keep track of best scoring sets
            highest_score = 0.0
            highest_p = 0
            highest_route = [[] for l in range(iterations)]
            
            temp = np.zeros((22, 22))
            
            # store routes in one big list
            route = [[] for l in range(iterations)]
            
            # first determine best scoring route from the first set of start-end possibilities
            # then take that route into consideration at the next route etc.
            for m in range(iterations):
                # check all possibilities between two stations
                for possibility in reach[indexes[m]]:
                    # clear currect route for every possibility
                    route[m].clear()
                    
                    total_time = 0
                    time = 0
                    
                    visited_connections = temp.copy()
                    
                    # determine the critical percentage and min amount for a route
                    for station in possibility:
                        if possibility.index(station) == 0:
                            route[m].append(station)
                        
                        else:
                            time = int(main_array[stations.index(possibility[possibility.index(station) - 1])][stations.index(station)])
                            
                            if (total_time + time) > 120:
                                break
                            
                            else:
                                route[m].append(station)
                                visited_connections[stations.index(possibility[possibility.index(station) - 1])][stations.index(station)] += 1
                                visited_connections[stations.index(station)][stations.index(possibility[possibility.index(station) - 1])] += 1
                                total_time += time
                    
                    route[m].insert(0, total_time)
                    
                    # score function parameters
                    percentage, missed    = object.p(main_array, visited_connections, stations, critical_stations)
                    t   = iterations
                    min = object.min(route, (m+1))
                    
                    final_score = score(percentage, t, min)
                    
                    if final_score > highest_score:
                        highest_score = final_score
                        highest_route[m] = route[m].copy()
                        highest_visited = visited_connections.copy()
    
#        temp = highest_visited.copy()
#        route = highest_route.copy()
                    temp = highest_visite
                    route = highest_route

        if highest_score > all_time_highest_score:
            all_time_highest_score = highest_score
            for a in range(iterations):
                all_time_highest_route[a] = highest_route[a].copy()
            all_time_highest_visited = highest_visited.copy()
            print(all_time_highest_score)

        writer.writerow([int(round((all_time_highest_score - 9859.99), 5)*100000)])

    for row in all_time_highest_route:
        print(row)
        
#        print(all_time_highest_visited)
#        all_time_highest_p, missed = object.p(main_array, all_time_highest_visited, stations, critical_stations)
        all_time_highest = main_array, stations, critical_stations
        
#        print(all_time_highest_p)

        return all_time_highest_route, all_time_highest_score
