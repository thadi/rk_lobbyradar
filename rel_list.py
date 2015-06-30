import pymongo
import pprint
pp = pprint.PrettyPrinter(indent=4)
con = pymongo.Connection()
entities = con.wissenrep.entities
relations = con.wissenrep.relations

types = {}

for rel in relations.find():
    t = rel.get('type')
    if(t not in types): types[t] = 0
    types[t] += 1

pp.pprint(types)
