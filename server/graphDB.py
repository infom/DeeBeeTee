import os
import json

from py2neo import Node, NodeSelector, Graph
import collections

graph = Graph(user="neo4j", password="fgfHQ6PFzWNx", host="194.87.236.140", bolt=True)
selector = NodeSelector(graph)

def getBalanceDetails(nodeName):

    target = selector.select("Person", name=nodeName).first()
    out_rels = graph.match(start_node=target, rel_type="TX")
    in_rels = graph.match(end_node=target, rel_type="TX")

    details = collections.defaultdict(dict)
    b_out = 0
    b_in = 0

    for tx in out_rels:
        b_out += tx["tx"]
        details[tx.end_node()["name"]]["out"] = b_out
        print(nodeName, "-----> ", tx.end_node()["name"], "----->", b_out)

    for tx in in_rels:
        b_in += tx["tx"]
        details[tx.start_node()["name"]]["in"] = b_in
        print(nodeName, "<----- ", tx.start_node()["name"], "----->", b_out)

    b_out = 0
    b_in = 0

    return json.dumps(dict(details))

'''
from neomodel import (config, StructuredNode, StructuredRel, StringProperty, IntegerProperty, DateTimeProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom)

username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

config.DATABASE_URL = 'bolt://'+username+':'+password+'@194.87.236.140:7687'

class TransactionsRel(StructuredRel):
    since = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    tx = IntegerProperty()
'''
'''
class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    balance = IntegerProperty(index=True, default=0)
    tx = RelationshipTo('Person', 'TX', model=TransactionsRel)
'''
'''
class UserMixin(object):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    #balance = IntegerProperty(index=True, default=0)


class BalanceMixin(object):
    credit_balance = IntegerProperty(index=True, default=0)
    debit_balance = IntegerProperty(index=True, default=0)
    balance = IntegerProperty(index=True, default=0)

    tx = RelationshipTo('Person', 'TX', model=TransactionsRel)

    def credit_account(self, amount):
        self.credit_balance = self.credit_balance + int(amount)
        self.balance = self.balance + self.credit_balance
        self.save()

    def debit_account(self, amount):
        self.debit_balance = self.debit_balance + int(amount)
        self.balance = self.balance - self.debit_balance
        self.save()

class Person(StructuredNode, UserMixin, BalanceMixin):
    pass
'''
