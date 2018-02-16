import json
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

import urllib.parse
import httplib2

http = httplib2.Http()

username = 'remote'
password = 'fgfHQ6PFzWNx'

client = MongoClient('mongodb://%s:%s@127.0.0.1' % (username, password))

db = client.test_database

users_json_file = open('users.json')
users_data = json.load(users_json_file)

transactions_json_file = open(transactions.json)
transactions_data = json.load(transactions_json_file)

users = db.users
transactions = db.transactions

def importUsers(data):

    url = 'http://127.0.0.1:5001/v1/users'

    for user in data:
        user.pop('uid', None)
        user.pop('limit', None)

        req_body = user
        headers = {'Content-type': 'application/json'}
        response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(req_body))
        print(response)
        time.sleep(1)


def importTransactions(data):
    url = 'http://127.0.0.1:5001/v1/transactions'
    for transaction in data:
        from_user = users.find_one({"username": transaction.from_user}, {'_id':1})
        to_user = users.find_one({"username":transaction.to_user}, {'_id':1})

        transaction.pop('tid', None)
        transaction['from_user'] = from_user
        transaction['to_user'] = to_user

        req_body = transaction
        headers = {'Content-type': 'application/json'}
        response, content = http.request(url, 'POST', headers=headers, body=urllib.parse.urlencode(req_body))
        print(response)
        time.sleep(1)
