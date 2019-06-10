import sys
import csv
import re
import networkx as nx
import networkx_TSM
import generate_retweet_graph
import louvain_communities
import subgraph_stats
import spreader_role
import second_level
import bel_ranks

# tweet_id = sys.argv[1]
tweet_id = '1118892161125240833'

id_dict = dict()
id_set = set()
ids_file = ''.join(['ids_l1_', tweet_id, '.txt'])
with open(tweet_id + '/' + ids_file) as infile:
    for line in infile:
        l_spl = re.split(r'[,]', line.rstrip())
        id_dict[l_spl[0]] = l_spl[1]
        id_set.add(l_spl[0])
        id_set.add(l_spl[1])

# Consider only those spreaders whose network could be extracted.
l_spreader = []
retweet_file = ''.join(['retweets_', tweet_id, '.txt'])
with open(tweet_id + '/' + retweet_file) as infile:
    for line in infile:
        l_spl = re.split(r'[,]', line.rstrip())
        if l_spl[2] in id_set:
            l_spreader.append(id_dict[l_spl[2]])


network_file = ''.join(['network_l1_', tweet_id, '.txt'])
G = nx.DiGraph()
with open(tweet_id + '/' + network_file) as infile:
    for line in infile:
        l_spl = re.split(',', line.rstrip())
        if len(l_spl) == 2:
            try:
                G.add_edge(id_dict[l_spl[0]], id_dict[l_spl[1]], weight=1)
            except KeyError:
                continue


networkx_TSM.TSM(tweet_id, G)
generate_retweet_graph.retweetGraph(tweet_id, id_dict)
louvain_communities.louvain_and_NBC(tweet_id, id_dict, G)
subgraph_stats.B_C_degree_stats(tweet_id, G)
spreader_role.sp_role(tweet_id, id_dict)
second_level.second_level_gen(tweet_id, id_dict)
bel_ranks.spread_edge_bel(tweet_id, id_dict, G, l_spreader)
