from rdflib import Graph
graph = Graph('Sleepycat')
graph.open('rdflib_data', create=True)

limit = 4
count = 0

#graph contains all triples in the store
#when using it in a for it return an triple with three elements (subject, property, object)
for source, relation, target in graph:
    triple = source + ' has relation ' + relation + ' to ' + target
    print(triple)
    if(limit != 0):
        count += 1
        if(count >= limit):
            break;
