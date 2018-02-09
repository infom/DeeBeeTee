import os
import json
import jinja2

from eve import Eve
from eve_swagger import swagger, add_documentation
from flask import render_template, send_from_directory, Response

from util import serializeDatetimeObjJSON, get_file

app = Eve(settings='settings.py')
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

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()+'/templates'),
])

app.jinja_loader = loader

def balance(username):
    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'uid': 1, '_id': 0})

    fromtsDict = list(transactions.aggregate([{ '$match' : { "from_uid" : uid['uid'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))
    totsDict = list(transactions.aggregate([{ '$match' : { "to_uid" : uid['uid'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))

    if fromtsDict == []:
        from_ts = 0
    else:
        from_ts = fromtsDict[0]['totalAmount']

    if totsDict == []:
        to_ts = 0
    else:
        to_ts = totsDict[0]['totalAmount']

    balance = from_ts - to_ts

@app.route('/v1/users/<path:username>/getBalance')
def getBalance(username):

    res = {'balance':balance(user)}
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/v1/users/<path:username>/getDetails')
def getDeatails(username):
    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'uid': 1, '_id': 0})

    bal = balance(username)
    print(bal)

    return Response(json.dumps(bal), mimetype='application/json')

@app.route('/v1/transactions/<path:username>')
def getTsByUser(username):

    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'uid': 1, '_id': 0})

    fromUidTs = list(transactions.find({'from_uid':uid['uid']}, {'to_uid':1, 'amount':1,'date':1, 'description':1, '_id':False}))
    toUidTs = list(transactions.find({'to_uid':uid['uid']}, {'from_uid':1,'amount':1, 'date':1, 'description':1, '_id':False}))

    results = {}
    results['from'] = serializeDatetimeObjJSON(fromUidTs)
    results['to'] = serializeDatetimeObjJSON(toUidTs)

    print(results)

    return Response(json.dumps(results), mimetype='application/json')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/files/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd()+'/server')
    return send_from_directory(os.path.join(root_dir, 'static', 'img'), filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
