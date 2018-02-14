from pyorient.ogm import Graph, Config
from pyorient.ogm.property import String, Float, DateTime
from pyorient.ogm.declarative import declarative_node, declarative_relationship
# Initialize Graph Database
graph = Graph(Config.from_url('localhost:2424/DeeBeeTee', 'deebeetee', 'deebeetee'))

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

#graph.create_all(Node.registry)
#graph.create_all(Relationship.registry)
# Bind Schema
graph.include(Node.registry)
graph.include(Relationship.registry)

def createNewNode(uid, username):
    graph.create_vertex(Person, name=username, uid=uid, credit_balance=0.0, debit_balance=0.0, balance=0.0)

    print('Create new node')

def createNewTransaction(data):

    from_uid=str(data['from_uid'])
    to_uid=str(data['to_uid'])
    since=data['date']
    tx=float(data['amount'])

    start_node = Person.objects.query(uid=from_uid).one()
    #SPerson.objects.query(uid=from_uid).one
    end_node = Person.objects.query(uid=to_uid).one()
    graph.create_edge(TransactionsRel, start_node, end_node, since=since, tx=tx)

    db = float(start_node.debit_balance) + tx
    b = float(start_node.debit_balance) - float(start_node.credit_balance)

    q = "UPDATE Person set debit_balance = %s balance = %s WHERE uid=%s" % db, b, from_uid
    print(q)
    graph.query(q)

    end_node.credit_balance = float(end_node.credit_balance) + tx
    end_node.balance = float(end_node.debit_balance) - float(end_node.credit_balance)

    print('Create new transaction')

def getBalanceDetails(username):
    pass
def getUserBalance(username):
    pass
