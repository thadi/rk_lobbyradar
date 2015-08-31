from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

def check_relation_type(relation_type, display = 5):
    relation_cursor = Relations.find({'type': relation_type})
    general_count = 0
    person_to_org = 0
    org_to_org = 0
    errors = 0

    for relation in relation_cursor:
        if len(relation['entities']) < 2:
            errors += 1
            continue
        source_id = relation['entities'][0]
        target_id = relation['entities'][1]
        source = Entities.find_one({'_id': ObjectId(source_id)})
        target = Entities.find_one({'_id': ObjectId(target_id)})
        if source and target:
            if source['type'] == 'person' and target['type'] == 'entity':
                person_to_org += 1
            elif source['type'] == 'entity' and target['type'] == 'entity':
                org_to_org += 1
            else:
                errors += 1
            if general_count < display:
                print source['name'] + ' (' + source['type'] + ')' + " has relation " + relation_type + ' to ' + target['name'] + ' (' + target['type'] + ')'
                print "\n"
        general_count += 1
    print "stats for relation type " + relation_type
    print "count relation: " + str(general_count)
    print "\t person to organization: " + str(person_to_org)
    print "\t organization to organization: " + str(org_to_org)
    print "\t errors: " + str(errors)

check_relation_type('member', 5)
