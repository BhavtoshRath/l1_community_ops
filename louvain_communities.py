"""generates two files:
louvain_: Each line contains community members.
com_NBC_: Generates dictionary of Core, Boundary, Neighbor for each community"""

import re
import networkx as nx
import community as com
from collections import defaultdict
import json
import csv
import sys


def louvain_and_NBC(tweet_id, G, l_spreaders):

    s_spreaders = set(l_spreaders)

    print('Running Louvain.....')
    louvain_file = ''.join(['louvain_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + louvain_file, 'w') as f:
        writer = csv.writer(f)
        part = com.best_partition(G.to_undirected())
        # cluster_set = set(part.values())
        # cluster_list = list(cluster_set)
        cluster = defaultdict(set)
        for node in part:
            cluster[part[node]].add(node)
        for c in cluster:
            l = list(cluster[c])
            writer.writerow(l)

    graph_nodes = set(G.nodes())
    print('No. of clusters:', len(cluster.keys()))
    with open(tweet_id + '/' + 'com_NBC_l1_'+tweet_id+'.txt', 'w') as f:
        for cl in cluster:
            print('Running for cluster: ', cl)
            # H = G.subgraph(cluster[cl])
            d = dict()
            d['cl'] = cl
            cluster_nodes = set(cluster[cl])
            infected_nodes = s_spreaders.intersection(cluster_nodes)
            # boundary_edges_out = list(nx.edge_boundary(G, graph_nodes.difference(cluster_nodes), cluster_nodes))
            boundary_edges_in = list(nx.edge_boundary(G, cluster_nodes, graph_nodes.difference(cluster_nodes)))
            boundary_nodes = set([str(i[0]) for i in boundary_edges_in])
            in_neighbor_nodes = set([str(i[1]) for i in boundary_edges_in])
            # out_neighbor_nodes = set([str(i[0]) for i in boundary_edges_out])
            core_nodes = (cluster_nodes.difference(boundary_nodes))
            d['core'] = list(core_nodes)
            d['inf_core'] = list(core_nodes.intersection(infected_nodes))
            d['boundary'] = list(boundary_nodes)
            d['inf_boundary'] = list(boundary_nodes.intersection(infected_nodes))
            d['neighbor'] = list(in_neighbor_nodes)
            d['inf_neighbor'] = list(in_neighbor_nodes.intersection(s_spreaders))
            dict_str = json.dumps(d)
            f.write(dict_str + '\n')





