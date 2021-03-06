import os
from eve import Eve
from flask import render_template, send_from_directory, Response
import jinja2
import json

#from neomodel import OUTGOING, INCOMING
#from neomodel.match import Traversal
from graphClient import getBalanceDetails, getUserBalance, createNewNode, createNewTransaction
#from py2neo import Node, NodeSelector, Graph
#import collections

def befor_insert_users(items):
    print(items)
    for i in items:
        i['username'] = i['username'].lower()
        print(i['username'])

def after_insert_users(items):
    users = app.data.driver.db['users']
    for i in items:
        uid = users.find_one({'username':i["username"]}, {'_id': 1, 'username':1})
        createNewNode(uid=str(uid["_id"]), username=uid["username"])

def after_insert_transactions(items):
    for i in items:
        createNewTransaction(i)

app = Eve(settings='settings.py')

app.on_insert_users += befor_insert_users
app.on_inserted_users += after_insert_users
app.on_inserted_transactions += after_insert_transactions

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()+'/templates'),
])
app.jinja_loader = loader

app.register_blueprint(swagger)

app.config['SWAGGER_INFO'] = {
    'title': 'DeeBeeTee API',
    'version': '1.0',
    'description': 'This is DeeBeeTee API Specification',
    'termsOfService': 'http://swagger.io/terms/',
    'contact': {
        'email': 'infominfom@gmail.com',
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
    },
    'schemes': ['http', 'https'],
}

@app.route('/v1/users/<path:username>/getBalance')
def getBalance(username):

    details = {'balance':getUserBalance(username)}
    return Response(json.dumps(details), mimetype='application/json')

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
