import json
import pyorient
from collections import Counter
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

def getUserBalance(username):
    query = client.query('select balance from Person where name='+repr(username))[0]

    return query.balance

def getBalanceDetails(username):

    node = Person.objects.query(name=username).one()

    out_tx = node.outE('transactionsrel')
    in_tx = node.inE('transactionsrel')

    if out_tx != None:
        outSum = convertToArrayAndSum(out_tx)
    if in_tx != None:
        inSum = convertToArrayAndSum(out_tx)

    print(outSum)
    return json.dumps({'status':'ok'})

def convertToArrayAndSum(arrayOfEdge, edgeType):

    counter = Counter()
    array = []

    if edgeType == outE:
        for edge in arrayOfEdge:
            array.append((edge.inV().name, edge.tx))
        for key, value in array:
            counter[key] += value

    if edgeType == inE:
        for edge in arrayOfEdge:
            array.append((edge.outV().name, edge.tx))
        for key, value in array:
            counter[key] += value

    return dict(counter)
