from pyorient.ogm import Graph, Config
from pyorient.ogm.property import String, Float, DateTime
from pyorient.ogm.declarative import declarative_node, declarative_relationship
# Initialize Graph Database
graph = Graph(Config.from_url('localhost:2424/DeeBeeTee', 'deebeetee', 'deebeetee'))

Node = declarative_node()
Relationship = declarative_relationship()

class TransactionsRel(Relationship):
    element_type = 'tx'
    since = DateTime()
    tx = Float()

class UserMixin(object):
    uid = String(indexed=True)
    name = String(indexed=True)

class BalanceMixin(object):
    credit_balance = Float(default=0, indexed=True)
    debit_balance = Float(default=0, indexed=True)
    balance = Float(default=0, indexed=True)

    def credit_account(self, amount):
        self.credit_balance = self.credit_balance + float(amount)
        self.balance = self.balance + self.credit_balance
        self.save()

    def debit_account(self, amount):
        self.debit_balance = self.debit_balance + float(amount)
        self.balance = self.balance - self.debit_balance
        self.save()

class Person(Node, UserMixin, BalanceMixin):
    element_type = 'person'

# Bind Schema
graph.include(Node.registry)
graph.include(Relationship.registry)

def createNewNode(uid, username):
    graph.create_vertex(Person, name=username, uid=uid)

    print('Create new node')

def createNewTransaction(data):

    from_uid=data['from_uid']
    to_uid=data['to_uid']
    since=data['date']
    tx=data['amount']

    start_node = Person.objects.query(uid=from_uid)
    end_node = Person.objects.query(uid=to_uid)
    print(start_node)
    graph.create_edge(TransactionsRel, start_node._id, end_node._id, since=since, tx=tx)

    start_node.debit_account(tx)
    end_node.credit_account(tx)

    print('Create new transaction')

def getBalanceDetails(username):
    pass
def getUserBalance(username):
    pass
