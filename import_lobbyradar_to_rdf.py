from rdflib import Graph
g = Graph('Sleepycat')

g.open('/home/thade/tmp/Wissenrep/lobbyradar_test', create=True)

import pymongo

c = pymongo.Connection()
relations = c.wissenrep.relations
entities = c.wissenrep.entities

base_entity = "http://www.example.com/entity/"
base_relation = "http://www.example.com/relation/"

file = open('lobbyradar_turtel', 'a')

for r in relations.find():
	entities_ids = r.get('entities')
	if(len(entities_ids) >= 2):
		entity_source = entities.find({'_id': entities_ids[0]})
		entity_target = entities.find({'_id': entities_ids[1]})
		if(entity_source.count() > 0 and entity_target.count() > 0):
			entity_source = entity_source.next()
			entity_target = entity_target.next()
			file.write('<' + base_entity + entity_source.get('_id').__str__() + '> ' + '<' + base_relation + r.get('type') + '> ' + '<' + base_entity + entity_target.get('_id').__str__() + '> . \n')
