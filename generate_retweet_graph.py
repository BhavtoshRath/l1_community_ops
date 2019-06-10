"""Generates all possible spread paths"""

import re
from collections import defaultdict
import csv
import sys


def retweetGraph(tweet_id, id_dict, l_spreaders):

    d = defaultdict(set)
    followers_file = ''.join(['followers_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + followers_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            d[id_dict[l_spl[1]]].add(id_dict[l_spl[0]])

    ret_graph_file = ''.join(['retweet_graph_', tweet_id, '.txt'])
    with open(tweet_id + '/' + ret_graph_file, 'w') as f:
        writer = csv.writer(f)
        print(len(l_spreaders))
        for i in range(0, len(l_spreaders)):
            for j in range(i + 1, len(l_spreaders)):
                source = l_spreaders[i]
                target = l_spreaders[j]
                if target in d[source]:
                    l = []
                    l.append(target)
                    l.append(source)
                    writer.writerow(l)