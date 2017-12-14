import csv
import numpy as np

class loadData():

    def __init__(self):
        # list of all stations
        self.stations = []
        self.connections = []
        self.critical = []
        self.criticalconnections = []
        
        # list of coordinates
        self.latitude = []
        self.longitude = []

    def loadDataHolland(self):
        # import data from Stations csv file
        with open('../csv/StationsHolland.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.stations.append(row[0])
                self.latitude.append(row[1])
                self.longitude.append(row[2])
                # create list of critical stations
                if "Kritiek" in row:
                    self.critical.append(row[0])

        # import data from Connections csv file
        with open('../csv/ConnectiesHolland.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.connections.append(row)

        # read latitude from csv file
        with open('../csv/StationsHolland.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.latitude.append(row[1])

        # read longitude from csv file
        with open('../csv/StationsHolland.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                self.longitude.append(float(row[2]))
        
        # hardcode an array of every station with only one connection
        self.end_of_the_line = ["Den Helder", "Dordrecht"]
        self.starting_stations = self.critical + self.end_of_the_line

    def createMatrix(self):

        # instantiate numpy array to store all connections and travel times
        self.array = np.zeros((22, 22))

        # fill in numpy array accordingly
        for station in self.stations:
            for connection in self.connections:
                if connection[0] == station:
                    for item in self.critical:
                        if connection[0] in self.critical:
                            if connection not in self.criticalconnections:
                                self.criticalconnections.append(connection)
                    row = self.stations.index(station)
                    column = self.stations.index(connection[1])
                    self.array[row][column] = connection[2]
                if connection[1] == station:
                    if connection[1] in self.critical:
                        if connection not in self.criticalconnections:
                            self.criticalconnections.append(connection)
                    row = self.stations.index(station)
                    column = self.stations.index(connection[0])
                    self.array[row][column] = connection[2]
