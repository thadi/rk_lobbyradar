import pymongo
from pymongo import MongoClient
from bson.son import SON
from bson.objectid import ObjectId

import rdflib
from rdflib import Graph, Literal, BNode, Namespace, RDF, RDFS, URIRef
FOAF = Namespace('http://xmlns.com/foaf/0.1/')
DC = Namespace('http://purl.org/dc/elements/1.1/')
ORG = Namespace("http://www.w3.org/ns/org#")
CGOV = Namespace('http://reference.data.gov.uk/def/central-government/')

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

rdf_type = {"person": FOAF.Person, "entity": ORG.Organization}
rdf_property_keys = {
    'member': 'Mitglied member mitglied'.split(' '),
    'executive': 'Vorsitzender ececutive executive'.split(' '),
    'connection': 'Bundesdatenschutzbeauftragte Hausausweise consulting lobbyist publication sponsoring'.split(' '),
    'association': 'association'.split(' '),
    'donation': 'donation'.split(' '),
    'committee': 'committee'.split(' '),
    'activity': 'activity'.split(' '),
    'business': 'business'.split(' '),
    'subsidiary': 'Tochterfirma subsidiary subisdiary'.split(' '),
    'government': 'government'.split(' '),
    'position': 'Position position'.split(' ')
}
rdf_property = {
    'member': FOAF.member,
    'executive': ORG.executive,
    'connection': FOAF.connection,
    'association': ORG.association,
    'donation': ORG.donation,
    'committee': ORG.committee,
    'activity': FOAF.activity,
    'business': ORG.business,
    'subsidiary': ORG.subsidiary,
    'government': CGOV.government,
    'position': ORG.position
}

def get_property(property_key):
    if property_key in rdf_property:
        return rdf_property[property_key]
    return False

def get_property_key(relation_type):
    for key in rdf_property_keys:
        if relation_type in rdf_property_keys[key]:
            return key
    return False

def get_prop(relation_type):
    return get_property(get_property_key(relation_type))

map_got_donation = {}

def make_special_deklaration(key, source, target, sname, tname):
    if key == 'donation':
        if target not in map_got_donation.keys(): map_got_donation[target] = 0
        map_got_donation[target] += 1
        if(map_got_donation[target] > 5):
            g.add((target, RDF.type, CGOV.Party))
    elif key == 'government':
        g.add((source, RDF.type, CGOV.Politican))

g = Graph()

g.bind("dc", DC)
g.bind("foaf", FOAF)
g.bind("org", ORG)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
g.bind("cgov", CGOV)

g.parse('ontologie.ttl', format='turtle')

for entity in Entities.find({}):
    node = BNode()

    g.add((node, DC.identifier, Literal(entity["_id"])))
    g.add((node, RDF.type, rdf_type[entity['type']]))
    g.add((node, RDFS.label, Literal(entity["name"])))

for relation in Relations.find({}):

    if len(relation['entities']) < 2: continue;

    source = g.value(predicate=DC.identifier, object=Literal(str(relation['entities'][0])))
    target = g.value(predicate=DC.identifier, object=Literal(str(relation['entities'][1])))

    source_type = g.value(subject=source, predicate=RDF.type)
    target_type = g.value(subject=target, predicate=RDF.type)

    source_name = g.value(subject=source, predicate=RDFS.label)
    target_name = g.value(subject=target, predicate=RDFS.label)

    if not source or not target: continue
    if source_type == ORG.Organization and target_type == FOAF.Person:
        source, target = target, source
    prop = get_prop(relation['type'])
    make_special_deklaration(get_property_key(relation['type']), source, target, source_name, target_name)
    if(prop):
        g.add((source, prop, target))
    else:
        print(relation['type'])

print g.serialize(format='turtle')
