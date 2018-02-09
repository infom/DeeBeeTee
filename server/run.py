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

    in_ts = list(transactions.aggregate([{'$group': {'_id': "$to_uid", 'totalAmount': {'$sum': '$amount'}}}]))
    out_ts = list(transactions.aggregate([{'$group': {'_id': "$from_uid", 'totalAmount': {'$sum': '$amount'}}}]))

    balance = in_ts[0]['totalAmount'] - out_ts[0]['totalAmount']
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
