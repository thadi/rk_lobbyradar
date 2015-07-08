import pymongo

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

#comment in what collection you would like to iterate
collection_to_iterate = relations
#collection_to_iterate = entities

#how many elements shall be iterated over? 0 for all
limit = 1
count = 0
#find without filter arguments returns a cursor pointing at the first element of an list
#containing all relation elements (since we didnt apply a filter)
for current_object in collection_to_iterate.find():
    #current_object contains the current object (bson)
    #with current_object.get(<field_name>) you get the specefied field value
    print(current_object)
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
    items_list = list(items)
    items_list = [x.lower() for x in items_list]
    items_list = [str(x) for x in items_list]
    items_list = sorted(items_list)
    return items_list

print get_items(relations, "type")
print('done')
