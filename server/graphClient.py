import json
import pyorient
from ogm import graph, Person, TransactionsRel

client = pyorient.OrientDB("localhost", 2424)  # host, port

### open a connection (username and password)
client.connect("deebeetee", "deebeetee")

### create a database
#client.db_create("DeeBeeTee", pyorient.DB_TYPE_GRAPH, pyorient.STORAGE_TYPE_MEMORY)

### select to use that database
client.db_open("DeeBeeTee", "deebeetee", "deebeetee")



def createNewNode(uid, username):

    client.command('insert into Person set name='+repr(username)+', uid='+repr(uid))
    #graph.create_vertex(Person, name=username, uid=uid, credit_balance=0.0, debit_balance=0.0, balance=0.0)

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

    debitb = float(start_node.debit_balance) + tx
    startb = float(start_node.debit_balance) - float(start_node.credit_balance)

    print('start node', debitb, startb)

    creditb = float(end_node.credit_balance) + tx
    endb = float(end_node.debit_balance) - float(end_node.credit_balance)

    print('end node', creditb, endb)
    client.command('update Person set debit_balance='+repr(debitb)+', balance='+repr(startb)+' where uid='+repr(from_uid))
    client.command('update Person set credit_balance='+repr(creditb)+', balance='+repr(endb)+' where uid='+repr(to_uid))

    print('Create new transaction')

def getBalanceDetails(username):
    pass

def getUserBalance(username):
    balance = client.query('select balance from Person where name='+repr(username))

    for b in balance:
        print(balance[0])
        return balance
