#note: just delete the rdflib_data folder whe you want to clean the store

#import rdflib
from rdflib import Graph
#create a graph in sleepycat-mode (on hard-drive)
import rdflib

graph = Graph('Sleepycat')
#open a triplestore (relative - in your directory, named rdflib)
#will be created if doesnt exist
#(a folder with the name rdflib_data in the current directory)
graph.open('rdflib_data', create=True)

#connect to mongodb
import pymongo
connection = pymongo.MongoClient('localhost', 27017)
db = connection.lobbyradar
relations = db.relations
entities = db.entities

limit = 10
count = 0

#iterate over the relations
for current_relation in relations.find():
    #the entities field of a relation-objects contains a array with entity ids
    #"entites": [<id1>, <id2>]
    entities_ids = current_relation.get('entities')
    #we only want to continue if entities_ids has more than 2 elements
    #since some relation-objects are fault
    if len(entities_ids) >= 2:
        #with the ids we get the real entites-objects
        entity_source = entities.find({'_id': entities_ids[0]})
        entity_target = entities.find({'_id': entities_ids[1]})
        #we only want to continue if both objects exist
        #some relations-objects contain non-existing data
        if entity_source.count() > 0 and entity_target.count() > 0:
            #with the find()-function we get cursor pointing at a list
            #with in this case only one element (ids are unique)
            #but we have to call next() so it returns the first (and only)
            #element of the list
            entity_source = entity_source.next()
            entity_target = entity_target.next()
            entity_source_name = entity_source.get('name')
            entity_target_name = entity_target.get('name')
            relation_type = current_relation.get('type')
            #we add the data to our store
            graph.add((entity_source_name, relation_type, entity_target_name))
            if limit != 0:
                count += 1
                if count >= limit:
                    break;
print('done')
