from pyorient.ogm import Graph, Config
from pyorient.ogm.property import String, Float, DateTime
from pyorient.ogm.declarative import declarative_node, declarative_relationship
# Initialize Graph Database

graph = Graph(Config.from_url('plocal://localhost:2424//DeeBeeTee', 'deebeetee', 'deebeetee'))
print(graph)

Node = declarative_node()
Relationship = declarative_relationship()

class TransactionsRel(Relationship):
    element_plural = 'tx'
    element_type = 'tx'
    since = DateTime()
    tx = Float()

class Person(Node):
    element_plural = 'person'
    element_type = 'person'

    uid = String(indexed=True)
    name = String(indexed=True)

    credit_balance = Float(default=0.0, indexed=True)
    debit_balance = Float(default=0.0, indexed=True)
    balance = Float(default=0.0, indexed=True)

graph.create_all(Node.registry)
graph.create_all(Relationship.registry)
# Bind Schema
graph.include(Node.registry)
graph.include(Relationship.registry)
