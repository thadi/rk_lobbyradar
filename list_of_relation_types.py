import pymongo
connection = pymongo.MongoClient('localhost', 27017)
db = connection.lobbyradar
relations = db.relations

relationTypeMap = {}

for relation in relations.find():
    relationName = relation.get('type')
    if relationName not in relationTypeMap : relationTypeMap[relationName] = 0
    relationTypeMap[relationName] += 1

print(relationTypeMap)
