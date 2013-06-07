# -*- coding: utf-8 -*-

import MySQLdb

class DBAdaptor:
    def __init__(self):
        self.read_txt()
        self.connect = MySQLdb.connect(host=self.con[0], user=self.con[1], passwd=self.con[2], db=self.con[3])
        self.connect.cursorclass = MySQLdb.cursors.DictCursor
        self.cursor = self.connect.cursor()
        self.issue_insert('set names utf8')

    def read_txt(self):
        self.con = []
        f = open("data/db.conf")
        line = f.readline()
        while line:
            self.con.append(line.rstrip())
            line = f.readline()

    def issue_select(self, query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except MySQLdb.Error, e:
            return e

    def issue_insert(self, query):
        try:
            self.cursor.execute(query)
            self.connect.commit()
        except MySQLdb.Error, e:
            # Duplicate entry
            if e[0] == 1062:
                pass
            else:
                return e

    def insert_user(self, user_id, screen_name, latitude, longitude):
        if latitude == None and longitude == None:
            query = "INSERT INTO users VALUES (%s, '%s', NULL, NULL)" % (user_id, screen_name)
        else:
            query = "INSERT INTO users VALUES (%s, '%s', %s, %s)" % (user_id, screen_name, latitude, longitude)
        self.issue_insert(query)

    def insert_edge(self, src_id, dst_id):
        query = "INSERT INTO graph VALUES (%s, %s)" % (src_id, dst_id)
        self.issue_insert(query)

    def get_followers(self, user_id):
        query = "SELECT src_id FROM graph WHERE dst_id = %s" % user_id
        return [row['src_id'] for row in self.issue_select(query)]
    def get_friends(self, user_id):
        query = "SELECT dst_id FROM graph WHERE src_id = %s" % user_id
        return [row['dst_id'] for row in self.issue_select(query)]

    def get_users(self, n):
        query = "SELECT * FROM users LIMIT %s" % n 
        results = self.issue_select(query)
        users = {}
        for result in results:
            users[result['id'] = result
        return users
    def get_labeled_users(self, n):
        query = "SELECT * FROM users WHERE latitude is not null LIMIT %s" % n 
        results = self.issue_select(query)
        users = {}
        for result in results:
            users[result['id'] = result
        return users

    def insert_dominance(self, user_id, dominance_type, n, mean, variance):
        query = "INSERT INTO dominance VALUES (%s, %s, %s, %s, %s, %s)" % (user_id, dominance_type, n, mean[0], mean[1], variance)
        self.issue_insert(query)

    def get_neighbors_dominane_distributions(self, user_id, f0):
        """ get in-dominance distributions """
        in_dominance_distributions = []
        in_query = "select points, variance, latitude, longitude from graph, dominance where src_id = %s and dst_id = dominance.id and type = 1 and points > %s" % (user_id, f0)
        results = self.issue_select(in_query)
        for result in results:
            entry = {'centrality': result['points'], 'variance': result['variance'], 'center': (result['latitude'], result['longitude'])}
            in_dominance_distributions.append(entry)

        """ get out-dominance distributions """
        out_dominance_distributions = []
        out_query = "select src_id as id, points, variance, latitude, longitude from graph, dominance where dst_id = %s and src_id = dominance.id and type = 0 and points > %s" % (user_id, f0)
        results = self.issue_select(out_query)
        for result in results:
            entry = {'centrality': result['points'], 'variance': result['variance'], 'center': (result['latitude'], result['longitude'])}
            out_dominance_distributions.append(entry)

        return (in_dominance_distributions, out_dominance_distributions)

