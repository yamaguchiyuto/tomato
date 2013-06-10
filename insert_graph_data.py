from lib.db import DBAdaptor

db = DBAdaptor()

graph_file = 'backup/data/network.txt'

for line in open(graph_file, 'r'):
    src_id, dst_id = line.rstrip().split('\t')
    db.insert_edge(src_id, dst_id)
