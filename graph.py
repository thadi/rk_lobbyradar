import rdflib
from rdflib import Graph

g = Graph()
g.parse('import.ttl', format='turtle')
