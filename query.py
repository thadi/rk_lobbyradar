import networkx as nx
import matplotlib.pyplot as plt
import rdflib
from rdflib import Graph

g = Graph()
g.parse('import.ttl', format='turtle')

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
    SELECT ?d ?rel ?c ?rel_2 ?g
    WHERE {
          ?a rdf:type cgov:Politican .
          ?f rdf:type cgov:Party .
          ?a ?rel ?b .
          ?b ?rel_2 ?f .
          ?a rdfs:label ?d .
          ?f rdfs:label ?g .
          ?b rdfs:label ?c .
    }
    LIMIT 100
    """)
#for s,p,t in qres:
#    print(s)
#    print(p)
#    print(t)
#    print('-----------')
#plot_triples([ (con[0].toPython(), con[1].toPython(), con[2].toPython()) for con in qres ])
rel = []
for pol, r_p_pa, pa, r_pa_pp, pp in qres:
    rel.append((pol, r_p_pa, pa))
    rel.append((pa, r_pa_pp, pp))

#for s in qres:
#    for e in s:
#        print e,
#    print ""

plot_triples(rel)
