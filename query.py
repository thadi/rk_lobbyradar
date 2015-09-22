import networkx as nx
import matplotlib.pyplot as plt
import graph

g = graph.g

def plot(network, figsize=(20,10)):
    G = nx.Graph()
    for connection in network:
        sub = connection[0]
        G.add_node(sub, typ='sub')
        if(len(connection) > 2 and connection[1] != None):
            obj = connection[1]
            G.add_node(obj, typ='obj')
            if(len(connection) > 3 and connection[2] != None):
                pro = connection[2]
            else:
                pro = "connection"
            G.add_edge(obj, sub, label=pro)
    plt.rcParams['figure.figsize'] = figsize
    plt.rcParams['font.family'] = 'sans-serif'
    nx.draw_networkx(G, node_size=600, linewidths=0, font_size=16)
    plt.show()

def entity_has_type(entity, type, graph = g):
    query = """
        SELECT ?a
        WHERE {
              ?a rdfs:label "%s" .
              ?a rdf:type %s .
        }
        """ % (entity.encode('utf-8'), type)
    query_result = graph.query(query)
    return True if len(query_result) > 0 else False

def entities_of_type(type, graph = g):
    query = """
        SELECT ?b
        WHERE {
              ?a rdf:type %s .
              ?a rdfs:label ?b .
        }
        """ % type
    query_result = graph.query(query)
    result = []
    for a in query_result:
        result.append(a[0].value)
    return result

def find_entity(entity, graph = g):
    query = """
        SELECT ?b
        WHERE {
              ?a rdfs:label ?b .
              FILTER(regex(lcase(str(?b)), ".*?%s.*?", "i"))
        }
        """ % entity.lower()
    query_result = graph.query(query)
    result = []
    for a in query_result:
        result.append((a[0].value, None, None))
    return result

def find_entity_with_type(entity, rdf_type, graph = g):
    query = """
        SELECT ?c
        WHERE {
              ?a rdf:type %s .
              ?a rdfs:label ?c .
              FILTER(regex(lcase(str(?c)), ".*?%s.*?", "i"))
        }
        """ % (rdf_type, entity.lower())
    query_result = graph.query(query)
    result = []
    for a in query_result:
        result.append((a[0].value, None, None))
    return result

def find_person(entity, graph = g):
    return find_entity_with_type(entity, 'foaf:Person')

def find_politican(entity, graph = g):
    return find_entity_with_type(entity, 'cgov:Politican')

def find_organization(entity, graph = g):
    return find_entity_with_type(entity, 'org:Organization')

def find_party(entity, graph = g):
    return find_entity_with_type(entity, 'cgov:Party')

def entity_object_relation(entity, relation, graph = g):
    query = """
        SELECT ?b ?e ?c
        WHERE {
              ?a rdfs:label "%s" .
              ?a rdfs:label ?b .
              ?d %s ?a .
              ?d rdfs:label ?e .
        }
        """ % (entity, relation)
    query_result = graph.query(query)
    result = []
    for a,b,c in query_result:
        result.append((a.value, b.value, relation))
    return result

def entity_subject_relation(entity, relation, graph = g):
    query = """
        SELECT ?b ?e ?c
        WHERE {
              ?a rdfs:label "%s" .
              ?a rdfs:label ?b .
              ?a %s ?d .
              ?d rdfs:label ?e .
        }
        """ % (entity, relation)
    query_result = graph.query(query)
    result = []
    for a,b,c in query_result:
        result.append((a.value, b.value, relation))
    return result

def entity_relation(entity, relation, graph = g):
    return entity_subject_relation(entity, relation) + entity_object_relation(entity, relation)

def politicans_of_party(party, graph = g):
    env_party = network_entity_level(party, 2)
    result = []
    for (s,o,p) in env_party:
        if(entity_has_type(o, 'cgov:Politican')):
            result.append((party, o, 'foaf:member'))
    return result

def network_subject(entity, graph = g):
    query = """
        SELECT ?b ?e ?c
        WHERE {
              ?a rdfs:label "%s" .
              ?a rdfs:label ?b .
              ?a ?c ?d .
              ?d rdfs:label ?e .
        }
        """ % entity
    query_result = graph.query(query)
    result = []
    for a,b,c in query_result:
        result.append((a.value, b.value, c))
    return result

def network_object(entity, graph = g):
    query = """
        SELECT ?b ?e ?c
        WHERE {
              ?a rdfs:label "%s" .
              ?a rdfs:label ?b .
              ?d ?c ?a .
              ?d rdfs:label ?e .
        }
        """ % entity
    query_result = graph.query(query)
    result = []
    for a,b,c in query_result:
        result.append((a.value, b.value, c))
    return result

def network_entity(entity, graph = g):
    return network_subject(entity) + network_object(entity)

def network_entity_level(entity, level = 1, graph = g):
    end_result = network_entity(entity)
    current_level = end_result
    next_level = []
    for i in range(level - 1):
        for s,o,p in current_level:
            next_level.extend(network_entity(o))
        end_result.extend(next_level)
        current_level = next_level
        next_level = []
    return end_result

def connection(entity, target, max_level = 1, graph = g):
    queue = []
    path = []
    network = network_entity(entity)
    queue.extend([Node(o, 0, Node(s, -1, None, None), p) for (s,o,p) in network])
    for node in queue:
        if(node.name == target):
            current_node = node
            while(current_node.parent.name != entity):
                path.append((current_node.name, current_node.parent.name, current_node.con))
                current_node = current_node.parent
            path.append((current_node.name, current_node.parent.name, current_node.con))
            return path
        if(node.lvl >= max_level):
            return []
        element_network = network_entity(node.name)
        for s,o,p in element_network:
            if(not is_in_node_list(o, queue)):
                queue.append(Node(o , node.lvl + 1, node, p))

def is_in_node_list(name, node_list):
    for element in node_list:
        if(name == element.name):
            return True
    return False

class Node:
    def __init__(self, name, lvl, parent, con):
        self.name = name
        self.lvl = lvl
        self.parent = parent
        self.con = con
