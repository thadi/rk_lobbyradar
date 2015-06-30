from rdflib import Graph

g = Graph('Sleepycat')

g.open('/home/thade/tmp/Wissenrep/teststore', create=True)
