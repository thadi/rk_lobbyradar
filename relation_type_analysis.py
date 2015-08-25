from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

r_type = 'member'

rel_cur = Relations.find({'type': r_type})

count = 0

ue = 0
e = 0

for relation in rel_cur:
    if len(relation['entities']) < 2: continue
    sid = relation['entities'][0]
    tid = relation['entities'][1]
    sobj = Entities.find_one({'_id': ObjectId(sid)})
    tobj = Entities.find_one({'_id': ObjectId(tid)})
    if sobj and tobj:
        if sobj['type'] == tobj['type']: e += 1
        else: ue += 1
        if count < 10:
            print sobj['name'] + '(' + sobj['type'] + ')'
            print " has relation " + r_type + ' to '
            print tobj['name'] + '(' + tobj['type'] + ')'
            print "\n"
            count += 1
print "same type: " + str(e)
print "not same type: " + str(ue)
