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

client = MongoClient()
db = client.lobbyradar

Entities = db.entities
Relations = db.relations

rdf_type = {"person": FOAF.Person, "entity": ORG.Organization}

g = Graph()
g.bind("dc", DC)
g.bind("foaf", FOAF)
g.bind("org", ORG)
g.bind("rdf", RDF)
g.bind("rdfs", RDFS)
for entity in Entities.find({}):
    node = BNode()

    g.add((node, DC.identifier, Literal(entity["_id"])))
    g.add((node, RDF.type, rdf_type[entity['type']]))
    g.add((node, RDFS.label, Literal(entity["name"])))

for relation in Relations.find({}):

    if len(relation['entities']) < 2: continue;

    source = g.value(predicate=DC.identifier, object=Literal(str(relation['entities'][0])))
    target = g.value(predicate=DC.identifier, object=Literal(str(relation['entities'][1])))

    if not source or not target: continue

    g.add((source, FOAF.knows, target))

print("imported all entities and relations...")

def plot_triples(connections_triple, figsize=(20,10)):
    G = nx.Graph()
    for obj, prt, sub in connections_triple:
        G.add_node(obj, typ='obj')
        G.add_node(sub, typ='sub')
        G.add_edge(obj, sub, label=prt)
    colors = [ 'green' if G.node[node]['typ'] == 'obj' else 'red' for node in G.nodes() ]
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['font.family'] = 'sans-serif'
    nx.draw_networkx(G, node_color=colors, node_size=1000, linewidths=0, font_size=16)
    plt.show()

qres = g.query("""
    SELECT ?s ?p
    WHERE {
          ?s rdfs:label "Hubert Reiff" .
          ?p foaf:knows ?s
    }
    LIMIT 20
    """)
#for s,p,t in qres:
#    print(s)
#    print(p)
#    print(t)
#    print('-----------')
#plot_triples([ (con[0].toPython(), con[1].toPython(), con[2].toPython()) for con in qres ])
plot_triples(qres)
