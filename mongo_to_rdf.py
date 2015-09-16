import pymongo
from pymongo import MongoClient
from bson.son import SON
from bson.objectid import ObjectId
from pprint import pprint
import networkx as nx
import matplotlib.pyplot as plt

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

print("imported all entities and relations...")

def plot_set(entities, figsize=(20,10)):
    G = nx.Graph()
    for sub in entities:
        G.add_node(sub[0], typ='sub')
    colors = [ 'green' if G.node[node]['typ'] == 'obj' else 'red' for node in G.nodes() ]
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['font.family'] = 'sans-serif'
    nx.draw_networkx(G, node_color=colors, node_size=1000, linewidths=0, font_size=16)
    plt.show()

def plot_double(connections_double, prop, figsize=(20,10)):
    G = nx.Graph()
    for ops in connections_double:
        sub, obj = ops
        G.add_node(sub, typ='sub')
        G.add_node(obj, typ='obj')
        G.add_edge(obj, sub, label=prop)
    colors = [ 'green' if G.node[node]['typ'] == 'obj' else 'red' for node in G.nodes() ]
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['font.family'] = 'sans-serif'
    nx.draw_networkx(G, node_color=colors, node_size=1000, linewidths=0, font_size=16)
    plt.show()

def plot_triples(connections_triple, figsize=(20,10)):
    G = nx.Graph()
    for ops in connections_triple:
        sub, prt, obj = ops
        G.add_node(sub, typ='sub')
        G.add_node(obj, typ='obj')
        G.add_edge(obj, sub, label=prt)
    colors = [ 'green' if G.node[node]['typ'] == 'obj' else 'red' for node in G.nodes() ]
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['font.family'] = 'sans-serif'
    nx.draw_networkx(G, node_color=colors, node_size=1000, linewidths=0, font_size=16)
    plt.show()

qres = g.query("""
    SELECT ?an ?rel ?name
    WHERE {
          ?an rdfs:label "Angela Merkel" .
          ?an ?rel ?obj .
          ?obj rdfs:label ?name .
    }
    LIMIT 100
    """)
#for s,p,t in qres:
#    print(s)
#    print(p)
#    print(t)
#    print('-----------')
#plot_triples([ (con[0].toPython(), con[1].toPython(), con[2].toPython()) for con in qres ])
for s in qres:
    for e in s:
        print e,
    print ""
#plot_triples(qres)
