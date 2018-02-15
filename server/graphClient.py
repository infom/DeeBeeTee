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

    balance = {}
    if out_tx != []:
        outSum = convertToArrayAndSum(out_tx, edgeType='out')
    else:
        outSum = {'_':0}
    if in_tx != []:
        inSum = convertToArrayAndSum(in_tx, edgeType='in')
    else:
        inSum = {'_':0}

    # находим совпадения имен пользователей в словарях сумм входящих и исходящих транзакций
    equal_name = outSum.keys() & inSum.keys()

    # находим пользователей, которые есть только в исходящих транзакциях
    out_uniq = outSum.keys() - inSum.keys()

    # находим пользователей, которые есть только во входящих транзакциях
    in_uniq = inSum.keys() - outSum.keys()

    if len(equal_name) != 0:
        for e in equal_name:
            if e != '_':
                balance[e] = float(outSum[e]) - float(inSum[e])

    if len(out_uniq) != 0:
        for o in out_uniq:
            if o != '_':
                balance[o] = 0.0 - float(outSum[o])

    if len(in_uniq) != 0:
        for i in in_uniq:
            if i != '_':
                balance[i] = float(inSum[i])
                
    balance['_'] = float(node.balance)

    return json.dumps(balance)

def convertToArrayAndSum(arrayOfEdge, edgeType):

    counter = Counter()
    array = []

    if edgeType == 'out':
        for edge in arrayOfEdge:
            array.append((edge.inV().name, edge.tx))
        for key, value in array:
            counter[key] += value

    if edgeType == 'in':
        for edge in arrayOfEdge:
            array.append((edge.outV().name, edge.tx))
        for key, value in array:
            counter[key] += value

    return dict(counter)
