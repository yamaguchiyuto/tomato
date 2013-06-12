# -*- coding: utf-8 -*-

import sys
import math
import json
from lib.db import DBAdaptor

def norm_pdf(x, mean, var):
    """ avoiding the case var = 0 """
    p = (1/(2*math.pi*(var+1))) * math.exp(( (x[0] - mean[0])**2 + (x[1] - mean[1])**2 ) / (-2 * (var+1)))
    return p

def mixture_weight(centrality_sum, component):
    return component['centrality'] / float(centrality_sum)

def find_mode(lmm):
    max_prob = -1
    mode = None
    for component in lmm['components']:
        candidate = component['center']
        p = sum([norm_pdf(candidate, c['center'], c['variance']) * mixture_weight(lmm['centrality_sum'], c) for c in lmm['components']])
        if p > max_prob:
            max_prob = p
            mode = candidate
    return (mode, max_prob)

def make_lmm(user_id, c0, db):
    lmm = {'centrality_sum': 0, 'components':[]}

    """ each entry's form: {'centrality': xxx, 'variance': yyy, 'center': (lat, longi)} """
    in_dominance_distributions, out_dominance_distributions = db.get_neighbors_dominance_distributions(user_id, c0)

    centrality_sum = 0
    for dom_dist in in_dominance_distributions:
        lmm['centrality_sum'] += dom_dist['centrality']
        lmm['components'].append(dom_dist)
    for dom_dist in out_dominance_distributions:
        lmm['centrality_sum'] += dom_dist['centrality']
        lmm['components'].append(dom_dist)
        
    return lmm

if len(sys.argv) < 2:
    print "[USAGE]: python %s [c0]" % sys.argv[0]
    exit()

db = DBAdaptor()

""" threshold value of centrality constraint """
c0 = float(sys.argv[1])

user_size = 10
users = db.get_users(user_size)
results = {'c0': c0, 'results': []}
for user_id in users:
    lmm = make_lmm(user_id, c0, db)
    inferred_location, confidence = find_mode(lmm)
    results['results'].append({'user_id': user_id, 'inferred_location': inferred_location, 'confidence': confidence, 'actual_location': (users[user_id]['latitude'], users[user_id]['longitude'])})
print json.dumps(results)
