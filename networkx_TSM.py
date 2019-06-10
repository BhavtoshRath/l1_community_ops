"""Generate TS for network"""

import networkx as nx
import re
import math
import csv
import sys

inv = 0.359
iter_count = 20
normChoice = 1


def TSM(tweet_id, G):

    vertices = G.nodes()
    print('n(nodes): ', len(vertices))
    print('n(edges): ', len(G.edges()))

    hti = {}
    htw = {}

    for node in vertices:
     hti[node] = 1 /float(len(vertices))
     htw[node] = 1 /float(len(vertices))


    def calcScores(vs, s, n, other_sc, flag):
     if flag == 'ti':
         for vertex in vs:
             s += inver(other_sc.get(vertex))*G[n][vertex]['weight']
     elif flag == 'tw':
         for vertex in vs:
             s += inver(other_sc.get(vertex))*G[vertex][n]['weight']
     return s


    def inver(a):
     return 1/float(1+a**inv)


    def normalize(userScores, choice):
     score_list = userScores.values()
     min_val = min(score_list)
     max_val = max(score_list)
     if choice == 0:  # min-max
         for user in userScores:
             userScores[user] = (userScores[user] - min_val)/float(max_val - min_val)


     elif choice == 1: # sum-of-squares
         norm_den = sum(i**2 for i in score_list)
         norm_den = math.sqrt(norm_den)
         for user in userScores:
             userScores[user] = userScores[user]/float(norm_den)

     return userScores


    i = 0
    while i < iter_count:
     print('iteration count: ', i+1)
     for node in vertices:
             """Calculate Scores for Trustingness"""
             # vsti = g.neighbors(node, mode=OUT)
             vsti = [ind[1] for ind in G.out_edges(node)]
             sc = calcScores(vsti, hti.get(node), node, htw, 'ti')
             hti[node] = sc

     for node in vertices:
             """Calculate Scores for Trustworthiness"""
             # vstw = g.neighbors(node, mode=IN)
             vstw = [ind[0] for ind in G.in_edges(node)]
             sc = calcScores(vstw, htw.get(node), node, hti, 'tw')
             htw[node] = sc

     i += 1

    norm_hti = normalize(hti, normChoice)
    norm_htw = normalize(htw, normChoice)

    TS_file = ''.join(['TS_network_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + TS_file, 'w') as f:
        writer = csv.writer(f)
        for i in vertices:
            l = []
            l.append(i)
            l.append(norm_hti[i])
            l.append(norm_htw[i])
            writer.writerow(l)
