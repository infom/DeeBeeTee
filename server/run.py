import os
from eve import Eve
from flask import render_template, send_from_directory
import jinja2
import json

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

    intsDict = list(transactions.aggregate([{ '$match' : { "from_uid" : uid['uid'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))
    outtsDict = list(transactions.aggregate([{ '$match' : { "to_uid" : uid['uid'] }}, {'$group': {'_id': None, 'totalAmount': {'$sum': '$amount'}}}]))

    if intsDict == []:
        in_ts = 0
    else:
        in_ts = intsDict[0]['totalAmount']

    if outtsDict == []:
        out_ts = 0
    else:
        out_ts = outtsDict[0]['totalAmount']

    balance = in_ts - out_ts
    res = {'balance':balance}
    return json.dumps(res)

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
