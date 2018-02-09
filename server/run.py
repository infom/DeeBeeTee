import os
import json
import jinja2

from eve import Eve
from flask import render_template, send_from_directory, Response

from util import serializeDatetimeObjJSON, get_file

app = Eve(settings='settings.py')

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()+'/templates'),
])

app.jinja_loader = loader

@app.route('/v1/users/<path:username>/getBalance')
def getBalance(username):
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
    res = {'balance':balance}
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/v1/transactions/<path:username>')
def getTsByUser(username):

    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'uid': 1, '_id': 0})

    fromUidTs = list(transactions.find({'from_uid':uid['uid']}, {'to_uid':1,'date':1, 'description':1, '_id':False}))
    toUidTs = list(transactions.find({'to_uid':uid['uid']}, {'from_uid':1,'date':1, 'description':1, '_id':False}))

    results = {}
    results['from'] = serializeDatetimeObjJSON(fromUidTs)
    print(results)
    results['to'] = serializeDatetimeObjJSON(toUidTs)

    return Response(results, mimetype='application/json')

@app.route('/docs/api')
def api_docs():
    return render_template('api.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/files/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd()+'/server')
    return send_from_directory(os.path.join(root_dir, 'static', 'img'), filename)

@app.route('/files/swagger/<path:filename>')
def serve_files(filename):
    root_dir = os.path.dirname(os.getcwd())
    yaml = get_file(root_dir, filename)
    return Response(yaml, mimetype='application/yaml')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
