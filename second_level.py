"""Creates 2nd level users files"""

import re
import sys
from collections import defaultdict
import csv


def second_level_gen(tweet_id, id_dict):
    k = 100

    s1 = set()
    s2 = set()
    s_final = set()
    '''Followers's file'''
    print('reading followers file...')
    fol_dict = defaultdict(list)
    followers_file = ''.join(['followers_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + followers_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            if len(l_spl) == 2:
                s1.add(id_dict[l_spl[1]])
                s2.add(id_dict[l_spl[0]])
                fol_dict[id_dict[l_spl[1]]].append(id_dict[l_spl[0]])

    file_1 = ''.join(['followers_stats_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + file_1, 'w') as f:
        writer = csv.writer(f)
        for user in fol_dict:
            user_list = fol_dict[user]
            writer.writerow([user, len(user_list)])
            if len(user_list) > int(k):
                s_final = s_final.union(set(user_list[0:k]))
            else:
                s_final = s_final.union(set(user_list))

    '''Friend's file'''
    print('reading friends file...')
    frnd_dict = defaultdict(list)
    friends_file = ''.join(['friends_l1_', tweet_id, '.txt'])
    # s_spreaders = set()
    with open(tweet_id + '/' + friends_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            if len(l_spl) == 2:
                s1.add(id_dict[l_spl[0]])
                s2.add(id_dict[l_spl[1]])
                frnd_dict[id_dict[l_spl[0]]].append(id_dict[l_spl[1]])

    file_2 = ''.join(['friends_stats_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + file_2, 'w') as f:
        writer = csv.writer(f)
        for user in frnd_dict:
            user_list = frnd_dict[user]
            writer.writerow([user, len(user_list)])
            if len(user_list) > int(k):
                s_final = s_final.union(set(user_list[0:k]))
            else:
                s_final = s_final.union(set(user_list))

    s = s2.difference(s1)
    print('level_two_unique_users_unsampled_count:', len(s))
    print('level_two_unique_users_sampled_count:', len(s_final))

    name_dict = dict()
    ids_file = ''.join(['ids_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + ids_file) as infile:
        for line in infile:
            l_spl = re.split(r'[,]', line.rstrip())
            name_dict[l_spl[1]] = l_spl[0]

    i = 0
    level_two_unique_users_sampled_file = ''.join(['sampled_l1_', tweet_id, '.txt'])
    with open(tweet_id + '/' + level_two_unique_users_sampled_file, 'w') as f:
        writer = csv.writer(f)
        s_temp = s_final.difference(s1) # Excluding extracted users of first level.
        for user in s_temp:
            i += 1
            writer.writerow(['x', i, name_dict[user]])

