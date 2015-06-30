import pymongo
from rdflib import Graph

g = Graph('Sleepycat')

g.open('/home/thade/tmp/Wissenrep/teststore', create=True)

con = pymongo.Connection()

def iter_rel():
    for cur in con.wissenrep.relations.find():
        rel = cur
        rel_enitities = rel.get('entities')

        if(len(rel_enitities) >= 2):
            e1o = con.wissenrep.entities.find({'_id': rel_enitities[0]})
            e2o = con.wissenrep.entities.find({'_id': rel_enitities[1]})

            if(e1o.count() > 0 and e2o.count() > 0):
                e1o = e1o.next()
                e2o = e2o.next()
                g.add((e1o.get('name'), rel.get('type'), e2o.get('name')))
                print('added new relation')
                #print("http://lobbyradar.com/foaf#" + e1o.get('name') + "http://lobbyradar.com/relation#" + rel.get('type') + "http://lobbyradar.com/foaf#" + e2o.get('name'))
        #rdflin.add(e1o.next().get('name'), rel.get('type'), .next().get('name'))

def ent_rel(ent):
    print(ent)

iter_rel()

print(list(g.triples(('PERI GmbH', None, None))))
