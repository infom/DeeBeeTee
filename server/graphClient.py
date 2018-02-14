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

    client.command("insert into Person set name = %s, uid = %s", username, uids)
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

    db = float(start_node.debit_balance) + tx
    b = float(start_node.debit_balance) - float(start_node.credit_balance)

    data = {
        "@Person": {
            "debit_balance": db,
            "balance": b
        }
    }

    graph.record_update(start_node._rid, data, start_node._version)

    end_node.credit_balance = float(end_node.credit_balance) + tx
    end_node.balance = float(end_node.debit_balance) - float(end_node.credit_balance)

    print('Create new transaction')

def getBalanceDetails(username):
    pass
def getUserBalance(username):
    pass
