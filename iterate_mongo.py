import pymongo
from pprint import PrettyPrinter
p = PrettyPrinter(4)

#connect to localhost
connection = pymongo.MongoClient('localhost', 27017)
#get lobbyradar as db
#make sure you have an db named lobbyradar
#mongorestore -db lobbyradar -collection ...
#------------------^^^^^^^
db = connection.lobbyradar
#relations collection
relations = db.relations
#entities collection
entities = db.entities

#how many elements shall be iterated over? 0 for all
limit = 5
def iterate_collection(collection, limit):
    count = 0
    #find without filter arguments returns a cursor pointing at the first element of an list
    #containing all relation elements (since we didnt apply a filter)
    for current_object in collection.find():
        #current_object contains the current object (bson)
        #with current_object.get(<field_name>) you get the specefied field value
        p.pprint(current_object)
        raw_input("press enter for next entry")
        if limit != 0:
            count += 1
            if count >= limit:
                break
'''
gets a collection and returns a normalized list with unique values
for a given key.
'''
def get_items(data, key):
    items = set()
    for row in data.find():
        items.add(row[key])
    return sorted([str(x.lower()) for x in list(items)])

#print get_items(entities, "type")
iterate_collection(entities, 0)
print('done')
