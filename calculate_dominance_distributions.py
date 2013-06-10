# -*- coding: utf-8 -*-

from lib.db import DBAdaptor
import lib.util as util

def get_points(neighbors, users):
    neighbor_points = []
    for neighbor_id in neighbors:
        if neighbor_id in users:
            """ if this user is in our dataset """
            neighbor = users[neighbor_id]
            if neighbor['latitude'] != None:
                """ if this user has his home location """
                neighbor_points.append((neighbor['latitude'], neighbor['longitude']))
    return neighbor_points

def calculate_dominance_distribution(neighbors, users):
    neighbor_points = get_points(neighbors, users)
    if len(neighbor_points) > 1:
        center = util.calc_median(neighbor_points)
        variance = util.calc_variance(center, neighbor_points)
        return (center, variance)
    else:
        return ((-1,-1),-1)

db = DBAdaptor()

user_size = 10000000
users = db.get_users(user_size)

for user_id in users:
    """ calculate in-dominance distribution """
    followers = db.get_followers(user_id)
    in_center, in_variance = calculate_dominance_distribution(followers, users)
    db.insert_dominance(user_id, 0, len(followers), in_center, in_variance)

    """ calculate out-dominance distribution """
    friends = db.get_friends(user_id)
    out_center, out_variance = calculate_dominance_distribution(friends, users)
    db.insert_dominance(user_id, 1, len(friends), out_center, out_variance)
