#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import sys
sys.path.append('../classes/')
sys.path.append('../functions/')
sys.path.append('../algorithms/')
import matplotlib.pyplot as plt

class score_integrated():

	def __init__(self, main_array, visited_connections, stations, route, critical_stations, trains, iteration):
		self.main_array = main_array
		self.visited_connections = visited_connections
		self.stations = stations
		self.route = route
		self.critical_stations = critical_stations
		self.trains = trains
		self.iteration = iteration
		self.t = self.t()
		self.min = self.min()
		self.p = self.p()
		self.totalscore = self.totalscore(self.p, self.t, self.min)

	def __float__(self):
		return self.totalscore

	def t(self):
		t = self.trains
		return t

	def min(self):
		min = 0
		
		for i in range(self.iteration):
			min += self.route[i][0]
		
		return min
            
	def p(self):
		if len(self.critical_stations) != len(self.stations):
			all_criticals = 0
			missed_criticals = 0

			# compare the t array to the main array to check for missed critical connections
			for i in range(len(self.stations)):
				if self.stations[i] in self.critical_stations:
					x = np.count_nonzero(self.main_array[i, :] > 0)
					all_criticals += x
					
					y = np.count_nonzero(self.visited_connections[i, :] > 0)
					if not x == y:
						missed_criticals += (x - y)
						
			p = ((all_criticals - missed_criticals)/all_criticals)
			
		else:
			all_criticals = 0
			missed_criticals = 0
		
			for i in range(len(self.visited_connections)):
				x = np.count_nonzero(self.main_array[i, :] > 0)
				all_criticals += x
				
				y = np.count_nonzero(self.visited_connections[i, :] > 0)
				if not x == y:
					missed_criticals += (x - y)
				
			p = ((all_criticals - missed_criticals)/all_criticals)	
		        
		return p

	def totalscore(self, p, t, min):
		totalscore = (p * 10000) - ((t * 20) + (min/10000))
    
		return totalscore
