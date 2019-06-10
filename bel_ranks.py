'''For every spreader edge (source to target), generates rank of target followers node
based on believability for all followers of source'''

import networkx as nx
import json
import csv
import re
import sys
from collections import defaultdict


def spread_edge_bel(tweet_id, id_dict, G, l_spreaders):

    print('reading TS file...')
    TS_dict = dict()
    TS_file = ''.join(['TS_network_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + TS_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            TS_dict[l_spl[0]] = [l_spl[1], l_spl[2]]

    retweet_graph_file = ''.join(['retweet_graph_', tweet_id, '.txt'])
    G_fol = nx.DiGraph()
    with open(tweet_id + '/' + retweet_graph_file) as infile:
        for line in infile:
            l_spl = re.split(',', line.rstrip())
            if len(l_spl) == 2:
                try:
                    G_fol.add_edge(l_spl[0], l_spl[1], weight=1)
                except KeyError:
                    continue

    spreader_with_no_paths = 0
    # with open(tweet_id + '/' +'demofile3.txt', 'a') as f:
    retweet_graph_ranks_file = ''.join(['spreaders_bel_stats_', tweet_id, '.txt'])
    with open(tweet_id + '/' + retweet_graph_ranks_file, 'w') as f:
        writer = csv.writer(f)
        for spreader in l_spreaders:
            d = dict()
            d['spreader'] = spreader
            print('Spreader:', spreader)
            in_edge_list = list(G.in_edges(spreader))
            d['follower_count'] = len(in_edge_list)
            in_edge_user_list = [[i[0], float(TS_dict[i[0]][0])] for i in in_edge_list]
            in_edge_sorted_list = sorted(in_edge_user_list, key=lambda x: x[1])
            # f.write('No. of followers for ' + spreader + ': ' + str(len(in_edge_sorted_user_list)) + '\n')
            inf_edge_list = list(G_fol.in_edges(spreader))
            d['next_spreaders_count'] = len(inf_edge_list)
            d['next_spreaders'] = [i[0] for i in inf_edge_list]
            if len(inf_edge_list) > 0:
                inf_edge_user_list = [[i[0], float(TS_dict[i[0]][0])] for i in inf_edge_list]
                inf_edge_sorted_list = sorted(inf_edge_user_list, key=lambda x: x[1])
                print(in_edge_sorted_list.index(inf_edge_sorted_list[0]))
                spreader_bel_rank = [(len(in_edge_sorted_list) - in_edge_sorted_list.index(i)) for i in inf_edge_sorted_list]
                d['spreader_bel_rank'] = sorted(spreader_bel_rank) # Ranked based on decsending order of bel. scores
                # summary: x/y - 'x' of top 'y' believing followers are spreaders.
                d['summary'] = str(len(inf_edge_sorted_list)) + '/' + str((len(in_edge_sorted_list) -
                                                               in_edge_sorted_list.index(inf_edge_sorted_list[0])))
                print(len(inf_edge_sorted_list), ' of top ', (len(in_edge_sorted_list) -
                                                               in_edge_sorted_list.index(inf_edge_sorted_list[0])), 'are spreaders')
            else:
                d['summary'] = 'No next spreaders'
                print(spreader, 'has not inf spread paths from it')
                spreader_with_no_paths += 1
            # f.write('No. of spreader followers for '+ spreader + ': ' + str(len(inf_edge_sorted_user_list)) + '\n')
            d_dump = json.dumps(d)
            f.write(d_dump + '\n')

    print('No. of spreaders with no paths from them', spreader_with_no_paths)





