import os
import json
from datetime import datetime, timedelta

from py2neo import Node, NodeSelector, Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedObjects
import collections

class BalanceMixin(object):
    credit_balance = Property()
    debit_balance = Property()
    balance = Property()


    def credit_account(self, amount):
        self.credit_balance = self.credit_balance + int(amount)
        self.balance = self.balance + self.credit_balance
        self.save()

    def debit_account(self, amount):
        self.debit_balance = self.debit_balance + int(amount)
        self.balance = self.balance - self.debit_balance
        self.save()

class Person(GraphObject, BalanceMixin):
    __primarykey__ = "uid"

    uid = Property()
    name = Property()

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name


graph = Graph(user="neo4j", password="fgfHQ6PFzWNx", host="194.87.236.140", bolt=True)
selector = NodeSelector(graph)

def createNode(uid, username):

    user = Person(uid=uid, name=username)

    print(user)

    graph.create(user)

def createTransaction(transaction):

    yesterday = datetime.now() - timedelta(days=1)

    from_uid = str(transaction["from_uid"])
    to_uid = str(transaction["to_uid"])

    start_node = selector.select("Person", uid=from_uid).first()

#        start_node.balance = start_node.balance - i["amount"]

    end_node = selector.select("Person", uid=to_uid).first()
#        end_node.balance = end_node.balance + i["amount"]

    rel = Relationship(start_node, 'TX', end_node, since=yesterday, tx=transaction["amount"])
    graph.create(rel)

    start_node.debit_account = ransaction["amount"]
    end_node.credit_account = transaction["amount"]
    start_node.push()
    end_node.push()


def getUserBalance(nodeName):

    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'uid': 1, '_id': 0})

    intsDict = list(transactions.aggregate([{ '$match' : { "from_uid" : uid['uid'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))
    outtsDict = list(transactions.aggregate([{ '$match' : { "to_uid" : uid['uid'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))

    if intsDict == []:
        in_ts = 0
    else:
        in_ts = intsDict[0]['totalAmount']

    if outtsDict == []:
        out_ts = 0
    else:
        out_ts = outtsDict[0]['totalAmount']

    balance = in_ts - out_ts
    res = {'balance':balance}
    return json.dumps(res)

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
