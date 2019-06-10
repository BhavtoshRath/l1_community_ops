"""For B and C of every community, generates count, in-degree and out-degree stats"""

import networkx as nx
import json
import os
import re
import sys


def B_C_degree_stats(tweet_id, G):
    i = 0
    cluster = dict()
    louvain_file = ''.join(['louvain_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + louvain_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            cluster[i] = set(l_spl)
            i += 1

    graph_nodes = set(G.nodes())

    with open(tweet_id + '/' +'B_C_degree_stats_l1_'+tweet_id+'.txt', 'w') as f:
        for cl in cluster:
            d = dict()
            print('for cl: ', cl)
            # H = G.subgraph(cluster[cl])
            d['cl'] = cl
            cluster_nodes = set(cluster[cl])
            # boundary_edges_out = list(nx.edge_boundary(G, graph_nodes.difference(cluster_nodes), cluster_nodes))
            boundary_edges_in = list(nx.edge_boundary(G, cluster_nodes, graph_nodes.difference(cluster_nodes)))
            boundary_nodes = set([str(i[0]) for i in boundary_edges_in])
            # in_neighbor_nodes = set([str(i[1]) for i in boundary_edges_in])
            # out_neighbor_nodes = set([str(i[0]) for i in boundary_edges_out])
            core_nodes = (cluster_nodes.difference(boundary_nodes))
            # d_H_list = [i[1] for i in H.degree()]
            # plot(np.asarray(d_H_list), tweet_id, cl, 'Degree dist.')
            d['nodes_count'] = len(cluster_nodes)
            d['boundary_count'] = len(boundary_nodes)
            d['core_count'] = len(core_nodes)

            ''' in-degree..'''
            in_d_boundary_nodes = G.in_degree(list(boundary_nodes))
            in_d_boundary_nodes_list = [i[1] for i in in_d_boundary_nodes]
            fq_in_d_boundary_nodes = {i: in_d_boundary_nodes_list.count(i) for i in set(in_d_boundary_nodes_list)}
            # plot(np.asarray(in_d_boundary_nodes_list), tweet_id, cl, 'in-d of b-nodes')
            print('fq_in_d_boundary_nodes: ', fq_in_d_boundary_nodes)
            d['B_in_d'] = fq_in_d_boundary_nodes

            in_d_core_nodes = G.in_degree(list(core_nodes))
            in_d_core_nodes_list = [i[1] for i in in_d_core_nodes]
            fq_in_d_core_nodes = {i: in_d_core_nodes_list.count(i) for i in set(in_d_core_nodes_list)}
            # plot(np.asarray(in_d_core_nodes_list), tweet_id, cl, 'in-d of c-nodes')
            print('fq_in_d_core_nodes: ', fq_in_d_core_nodes)
            d['C_in_d'] = fq_in_d_core_nodes

            ''' out-degree..'''
            out_d_boundary_nodes = G.out_degree(list(boundary_nodes))
            out_d_boundary_nodes_list = [i[1] for i in out_d_boundary_nodes]
            fq_out_d_boundary_nodes = {i: out_d_boundary_nodes_list.count(i) for i in set(out_d_boundary_nodes_list)}
            # plot(np.asarray(out_d_boundary_nodes_list), tweet_id, cl, 'out-d of b-nodes')
            print('fq_out_d_boundary_nodes: ', fq_out_d_boundary_nodes)
            d['B_out_d'] = fq_out_d_boundary_nodes

            out_d_core_nodes = G.out_degree(list(core_nodes))
            out_d_core_nodes_list = [i[1] for i in out_d_core_nodes]
            fq_out_d_core_nodes = {i: out_d_core_nodes_list.count(i) for i in set(out_d_core_nodes_list)}
            # plot(np.asarray(out_d_core_nodes_list), tweet_id, cl, 'out-d of c-nodes')
            print('fq_out_d_core_nodes: ', fq_out_d_core_nodes)
            d['C_out_d'] = fq_out_d_core_nodes

            dict_str = json.dumps(d)
            f.write(dict_str + '\n')



