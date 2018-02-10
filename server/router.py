import os
import json

from flask import render_template, send_from_directory, Response

from util import serializeJSON, get_file
import dbtApiServer.app as app

def balance(username):
    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'_id': 1})

    fromtsDict = list(transactions.aggregate([{ '$match' : { "from_uid" : uid['_id'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))
    totsDict = list(transactions.aggregate([{ '$match' : { "to_uid" : uid['_id'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))

    if fromtsDict == []:
        from_ts = 0
    else:
        from_ts = fromtsDict[0]['totalAmount']

    if totsDict == []:
        to_ts = 0
    else:
        to_ts = totsDict[0]['totalAmount']

    return from_ts - to_ts

@app.route('/v1/users/<path:username>/getBalance')
def getBalance(username):

    res = {'balance':balance(username)}
    return Response(json.dumps(res), mimetype='application/json')

@app.route('/v1/users/<path:username>/getDetails')
def getDeatails(username):
    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'uid': 1, '_id': 0})

    bal = balance(username)

    fromTsDict = list(transactions.find({'from_uid':uid['uid']}, {'to_uid':1, 'amount':1}))
    toTsDict = fromTsDict = list(transactions.find({'to_uid':uid['uid']}, {'from_uid':1, 'amount':1}))


    return Response(json.dumps(bal), mimetype='application/json')

@app.route('/v1/transactions/<path:username>')
def getTsByUser(username):

    users = app.data.driver.db['users']
    transactions = app.data.driver.db['transactions']

    uid = users.find_one({'username':username}, {'_id': 1})

    fromUidTs = list(transactions.find({'from_uid':uid['_id']}, {'to_uid':1, 'amount':1,'date':1, 'description':1, '_id':False}))
    toUidTs = list(transactions.find({'to_uid':uid['_id']}, {'from_uid':1,'amount':1, 'date':1, 'description':1, '_id':False}))

    results = {}
    results['from'] = serializeJSON(fromUidTs)
    results['to'] = serializeJSON(toUidTs)

    print(results)

    return Response(json.dumps(results), mimetype='application/json')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/files/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd()+'/server')
    return send_from_directory(os.path.join(root_dir, 'static', 'img'), filename)
