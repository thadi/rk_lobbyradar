from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

for relation in Relations.find({}):
    if len(relation['entities']) < 2: continue;
    sid = relation['entities'][0]
    tid = relation['entities'][1]
    sobj = Entities.find_one({'_id': ObjectId(sid)})
    tobj = Entities.find_one({'_id': ObjectId(tid)})
    if sobj and tobj:

        if tobj['type'] != sobj['type'] and relation['type'] == "government":
            print(sobj['type'] + " " + relation['type'] + " " + tobj['type'])
