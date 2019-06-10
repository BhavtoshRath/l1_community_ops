"""Generates all possible spread paths"""

import re
from collections import defaultdict
import csv
import sys


def retweetGraph(tweet_id, id_dict):
    s_spreaders = []
    retweet_file = ''.join(['retweets_', tweet_id, '.txt'])
    with open(tweet_id + '/' + retweet_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            if l_spl[2] in id_dict.keys():
                s_spreaders.append(id_dict[l_spl[2]])

    d = defaultdict(set)
    followers_file = ''.join(['followers_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + followers_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            d[id_dict[l_spl[1]]].add(id_dict[l_spl[0]])

    ret_graph_file = ''.join(['retweet_graph_', tweet_id, '.txt'])
    with open(tweet_id + '/' + ret_graph_file, 'w') as f:
        writer = csv.writer(f)
        print(len(s_spreaders))
        for i in range(0, len(s_spreaders)):
            for j in range(i + 1, len(s_spreaders)):
                source = s_spreaders[i]
                target = s_spreaders[j]
                if target in d[source]:
                    l = []
                    l.append(target)
                    l.append(source)
                    writer.writerow(l)