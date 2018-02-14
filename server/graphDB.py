from pyorient.ogm import Graph, Config
from pyorient.ogm.property import String, Decimal, DateTime
from pyorient.ogm.declarative import declarative_node, declarative_relationship
# Initialize Graph Database
graph = Graph(Config.from_url('localhost:2424/DeeBeeTee', 'deebeetee', 'deebeetee'))

Node = declarative_node()
Relationship = declarative_relationship()

# Retrive Schema from OrientDB
classes_from_schema = graph.build_mapping(Node, Relationship, auto_plural = True)

# Initialize Schema in PyOrient
graph.include(classes_from_schema)

class TransactionsRel(Relationship):
    element_type = 'tx'
    since = DateTime()
    tx = Decimal()

class UserMixin(object):
    uid = String(indexed=True)
    name = String(indexed=True)

class BalanceMixin(object):
    credit_balance = Property(default=0, indexed=True)
    debit_balance = Property(default=0, indexed=True)
    balance = Property(default=0, indexed=True)

    def credit_account(self, amount):
        self.credit_balance = self.credit_balance + int(amount)
        self.balance = self.balance + self.credit_balance
        self.save()

    def debit_account(self, amount):
        self.debit_balance = self.debit_balance + int(amount)
        self.balance = self.balance - self.debit_balance
        self.save()

class Person(Node, UserMixin, BalanceMixin):
    element_type = 'person'

def createNewNode(uid, username):
    graph.create_vertex(Person, name = username, uid = uid)

    print('Create new node')

def createNewTransaction(data):
    pass

def getBalanceDetails(username):
    pass
def getUserBalance(username):
    pass
