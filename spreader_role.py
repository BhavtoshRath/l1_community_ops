"""For every spreader check for which communities its is a C, B or N."""

import json
import os
import re
import sys
from collections import defaultdict


def sp_role(tweet_id,  l_spreaders):

    with open(tweet_id + '/' + 'spreader_role_l1_'+tweet_id+'.txt', 'w') as f:
        for spreader in l_spreaders:
            D = defaultdict(list)
            D['spreader'] = spreader
            com_NBC_file = ''.join(['com_NBC_l1_', tweet_id, '.txt'])
            with open(tweet_id + '/' + com_NBC_file) as infile:
                for line in infile:
                    d = json.loads(line)
                    d_keys = ['core', 'neighbor', 'boundary']
                    for key in d_keys:
                        value = d[key]
                        if spreader in value:
                            D[key].append(d['cl'])
            dict_str = json.dumps(D)
            print(D)
            f.write(dict_str + '\n')
