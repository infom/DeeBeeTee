import os
from eve import Eve
from flask import render_template, send_from_directory, Response
import jinja2
import json
from datetime import datetime, timedelta
#from neomodel import OUTGOING, INCOMING
#from neomodel.match import Traversal
from graphDB import getBalanceDetails, getUserBalance, Person, graph
#from py2neo import Node, NodeSelector, Graph
#import collections


def after_insert_users(items):

    users = app.data.driver.db['users']

    for i in items:

        uid = users.find_one({'username':i["username"]}, {'_id': 1, 'username':1})

        user = Person()
        user.uid = uid["_id"].toString()
        user.name = uid["username"]

        graph.create(user)


#        Person(uid=uid["_id"], name=uid["username"], balance=0).save()

        print("Create new node "+ i["username"])
'''
def after_insert_transactions(items):

    for i in items:

        yesterday = datetime.now() - timedelta(days=1)

        from_uid = i["from_uid"]
        to_uid = i["to_uid"]

        start_node = Person.nodes.get(uid=from_uid)

#        start_node.balance = start_node.balance - i["amount"]

        end_node = Person.nodes.get(uid=to_uid)
#        end_node.balance = end_node.balance + i["amount"]

        start_node.tx.connect(end_node, {'since': yesterday, 'tx': i["amount"]})

        start_node.debit_account(i["amount"])
        end_node.credit_account(i["amount"])
        start_node.save()
        end_node.save()

        rel = start_node.tx.all_relationships(end_node)

        for r in rel:
            print(r.start_node().name, "------>", r.end_node().name, "------>", r.tx)
'''
app = Eve(settings='settings.py')

app.on_inserted_users += after_insert_users
#app.on_inserted_transactions += after_insert_transactions

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()+'/templates'),
])
app.jinja_loader = loader


@app.route('/v1/users/<path:username>/getBalance')
def getBalance(username):

    details = getUserBalance(username)

@app.route('/v1/users/<path:username>/getDetails')
def getDetails(username):

    details = getBalanceDetails(username)


    return Response(details, mimetype='application/json')

@app.route('/docs/api')
def api_docs():
    return render_template('api.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/files/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd()+'/server')
    return send_from_directory(os.path.join(root_dir, 'static', 'img'), filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
