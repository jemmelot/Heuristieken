#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import random
import sys
sys.path.append('../classes/')
from loadData import loadData
from ScoreVariables import score_variables

userinputamount = input("How many Trains: ")
response = input("How many tests would you like to run: ")
trails = int(response)

for trail in range(trails):

    x = loadData()
    x.loadDataHolland()
    
#    # import data from Stations csv file
#    with open('../csv/StationsHolland.csv', 'r') as csvfile:
#        reader = csv.reader(csvfile)
#        for row in reader:
#            x.stations.append(row[0])
#            x.latitude.append(row[1])
#            x.longitude.append(row[2])
#            # create list of critical stations
#            if "Kritiek" in row:
#                x.critical.append(row[0])
#
#
#    # import data from Connections csv file
#    with open('../csv/ConnectiesHolland.csv', 'r') as csvfile:
#        reader = csv.reader(csvfile)
#        for row in reader:
#            x.connections.append(row)

    connectiontimes = [int(connection[2]) for connection in x.connections]


    # Scorefunctie: S = p*10000 - (t*20 + m/10000)
    # p het percentage van de bereden kritieke verbindingen
    # t het aantal treinen
    # m het totaal door alle treinen samen gereden aantal minuten in de lijnvoering.
    max_s = 10000.000
    max_t = -(7 * 20)
    max_m = -(120)
    max_p = max_s + max_t + max_m


    # instantiate numpy array
    array = np.zeros((22, 22))

    # fill in numpy array accordingly
    for station in x.stations:
        for connection in x.connections:
            if connection[0] == station:
                for item in x.critical:
                    if connection[0] in x.critical:
                        if connection not in x.criticalconnections:
                            x.criticalconnections.append(connection)
                row = x.stations.index(station)
                column = x.stations.index(connection[1])
                array[row][column] = connection[2]
            if connection[1] == station:
                if connection[1] in x.critical:
                    if connection not in x.criticalconnections:
                        x.criticalconnections.append(connection)
                row = x.stations.index(station)
                column = x.stations.index(connection[0])
                array[row][column] = connection[2]


    # calculate added value for station being critical
    val_critic = max_p / len(x.criticalconnections)

    # calculate added value for duration of connection
    # ECHTE VERSIE val_time = [float(x / 10000) for x in connectiontimes]
    val_time = [float(-z) for z in connectiontimes]


    #for trail in range(100):
    # give a value to each connection
    for connection in x.connections:
        if connection[0] in x.critical or connection[1] in x.critical:
            connection.append(val_critic)
        else:
            connection.append(0)
        connection.append("y")
        if connection[4] == "y":
            connection[4] = float(connection[2])
        connection.append(int(connection[3]) - connection[4])


    #print(connections)
    #print(val_time)

    # start greedy algorithm
    numbertracks = int(userinputamount)


    # get random starting stations
    trackstart = []
    max_lenght = 120

    for i in range(numbertracks):
        trackstart.append(random.randrange(0, 28))
    #    print(trackstart)

    routes = [[] for i in range(numbertracks)]
    #    print(routes)

    # set starting stations in routes
    counter = 0
    for track in trackstart:
        routes[counter].append(0)
        routes[counter].append(x.connections[track][0])
        counter += 1

    #    print(routes)


    counterrow = 0
    countercollum = 1
    routeended = [0] * numbertracks
    totalscore = numbertracks * -20

    for j in range(50):
        counterrow = 0
        for i in range(numbertracks):
            scorelist = []
            time = 0
            if routeended[i] == 0:
                for connection in x.connections:
                    if routes[counterrow][countercollum] == connection[0]:
                        scorelist.append(connection[5])
    #                        print(connection[0])
                    if routes[counterrow][countercollum] == connection[1]:
                        scorelist.append(connection[5])
    #                        print(connection[1])
    #                print(scorelist)
                bestnext = max(scorelist)
    #                print(bestnext)
                for connection in x.connections:
                    if routes[counterrow][countercollum] == connection[0]:
                        if connection[5] == bestnext:
                            time += connection[4]
                            if routes[counterrow][0] + connection[4] <= 120:
                                routes[counterrow].append(connection[1])
                                routes[counterrow][0] += connection[4]
                                totalscore += connection[3] - connection[4]
                                connection[5] += -connection[3] - 5
                                connection[3] = 0
                            else:
                                routeended[i] = 1
                    elif routes[counterrow][countercollum] == connection[1]:
                        if connection[5] == bestnext:
                            time += connection[4]
                            if routes[counterrow][0] + connection[4] <= 120:
                                routes[counterrow].append(connection[0])
                                routes[counterrow][0] += connection[4]
                                totalscore += connection[3] - connection[4]
                                connection[5] += -connection[3] - 5
                                connection[3] = 0
                            else:
                                routeended[i] = 1
            if routeended[0:numbertracks] == 1:
                break
            counterrow += 1
        countercollum += 1

    #    print('\n'.join(' '.join(map(str,sl)) for sl in connections))

#    print('\n'.join(' '.join(map(str,sl)) for sl in routes))
    #    print(routeended)
    print("")
    print "Trial: ", trail
    with open('greedyscores.csv', 'r') as myfile:
        last_line = myfile.readlines()[-1]
        last_line = float(last_line.rstrip('\n'))

    print "Highest Score: ", last_line
    print "Current Score: ", totalscore

    if totalscore > last_line:
        print("Result: Succes")
        with open('greedyscores.csv', 'a') as myfile:
            wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
            wr.writerow([totalscore])
        with open('greedyroute.csv', 'a') as myfile:
            wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
            wr.writerow([routes])
    else:
        print("Result: Fail")

with open('greedyroute.csv', 'r') as myfile:
    best_route = myfile.readlines()[-1]

print("")
print "The best route is: "
print(best_route)
print("")
print "It has a score of: ", last_line
print("")
