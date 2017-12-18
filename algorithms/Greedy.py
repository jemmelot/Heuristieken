
#!/usr/bin/python3
# https://github.com/jemmelot/Heuristieken.git

import numpy as np
import csv
import random
import sys
import os
import copy
sys.path.append('../classes/')
from createnetwerk import createNetwerk
from ScoreVariables import score_variables


def greedy(connections, criticalconnections, critical, trainamount, trials):

        
#    connectiontimes = [float(connection[2]) for connection in connections]
#
#    # Scorefunctie: S = p*10000 - (t*20 + m/10000)
#    # p het percentage van de bereden kritieke verbindingen
#    # t het aantal treinen
#    # m het totaal door alle treinen samen gereden aantal minuten in de lijnvoering.
#    max_s = 10000.000
#    max_t = -(7 * 20)
#    max_m = -(120)
#    max_p = max_s + max_t + max_m
#
#    # calculate added value for station being critical
#    val_critic = max_p / len(criticalconnections)
#
#    # calculate added value for duration of connection
#    val_time = [float(-z) for z in connectiontimes]
#
#    # give a value to each connection
#    for connection in connections:
#        if connection[0] in critical or connection[1] in critical:
#            connection.append(val_critic)
#        else:
#            connection.append(0)
#        connection.append("y")
#        if connection[4] == "y":
#            connection[4] = float(connection[2])
#        connection.append(int(connection[3]) - connection[4])

    # start greedy algorithm
    numbertracks = trainamount
    for trial in range(trials):
        copy_connections = copy.deepcopy(connections)
        print(copy_connections)
        
        # get random starting stations
        trackstart = []
        max_lenght = 120

        for i in range(numbertracks):
            trackstart.append(random.randrange(0, 28))
        route = [[] for i in range(numbertracks)]

        counter = 0
        for track in trackstart:
            route[counter].append(0)
            route[counter].append(copy_connections[track][0])
            counter += 1
        counterrow = 0
        countercollum = 1
        routeended = [0] * numbertracks
        totalscore = numbertracks * -20

        for j in range(50):
            counterrow = 0
            for i in range(numbertracks):
                scorelist = []
                scorelistname = []
                time = 0
                if routeended[i] == 0:
                    for connection in copy_connections:
                        if route[counterrow][countercollum] == connection[0]:
                            scorelist.append(connection[5])
                            scorelistname.append(connection[1])
                        if route[counterrow][countercollum] == connection[1]:
                            scorelist.append(connection[5])
                            scorelistname.append(connection[0])
                    bestnext = max(scorelist)
                    index = scorelist.index(max(scorelist))
                    bestnextname = scorelistname[index]
                    scorelist = []
                    scorelistname = []
                    for connection in copy_connections:
                        if route[counterrow][countercollum] == connection[0]:
                            if connection[5] == bestnext and connection[1] == bestnextname:
                                time += connection[4]
                                if route[counterrow][0] + connection[4] <= 120:
                                    route[counterrow].append(connection[1])
                                    route[counterrow][0] += connection[4]
                                    totalscore += connection[3] - connection[4]
                                    connection[5] += -connection[3] - 5
                                    connection[3] = 0
                                else:
                                    routeended[i] = 1
                        elif route[counterrow][countercollum] == connection[1]:
                            if connection[5] == bestnext and connection[0] == bestnextname:
                                time += connection[4]
                                if route[counterrow][0] + connection[4] <= 120:
                                    route[counterrow].append(connection[0])
                                    route[counterrow][0] += connection[4]
                                    totalscore += connection[3] - connection[4]
                                    connection[5] += -connection[3] - 5
                                    connection[3] = 0
                                else:
                                    routeended[i] = 1
                if routeended[0:numbertracks] == 1:
                    break
                counterrow += 1
            countercollum += 1
        
        
        print("")
        print ("Trial: ", trial)
        with open('./csv/greedyscores.csv', 'r') as myfile:
            last_line = myfile.readlines()[-1]
            last_line = float(last_line.rstrip('\n'))

        print ("Highest Score: ", last_line)
        print ("Current Score: ", totalscore)

        if totalscore > last_line:
            print("Result: Succes")
            with open('./csv/greedyscores.csv', 'a') as myfile:
                wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
                wr.writerow([totalscore])
            with open('./csv/greedyroute.csv', 'a') as myfile:
                wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
                wr.writerow([route])
        else:
            print("Result: Fail")

        with open('./csv/greedyalltrials.csv', 'a') as myfile:
            wr = csv.writer(myfile,sys.stdout, lineterminator='\n')
            wr.writerow([totalscore])

        with open('./csv/greedyroute.csv', 'r') as myfile:
            best_route = myfile.readlines()[-1]

    return route


