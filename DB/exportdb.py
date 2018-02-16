import json
import time
from pymongo import MongoClient
from bson.objectid import ObjectId

import urllib.parse
import httplib2

http = httplib2.Http()

username = 'remote'
password = 'fgfHQ6PFzWNx'

client = MongoClient("mongodb://remote:fgfHQ6PFzWNx@localhost:27017/deebeetee")

db = client['deebeetee']

users = db.users
transactions = db.transactions

users_json_file = open('users.json')
users_data = json.load(users_json_file)

transactions_json_file = open('transactions.json')
transactions_data = json.load(transactions_json_file)

def importUsers(data):

    url = 'http://127.0.0.1:5001/v1/users'

    for user in data:
        user.pop('uid', None)
        user.pop('limit', None)

        user['username'] = user['user'].lower()
        del user['user']
        print(user)

        req_body = user
        headers = {'Content-Type': 'application/json; charset=UTF-8'}
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(req_body))
        print(content)
        time.sleep(1)


def importTransactions(data):
    url = 'http://127.0.0.1:5001/v1/transactions'

    for transaction in data:
        from_user = users.find_one({"username": transaction['from_user'].lower()}, {'_id':1})
        to_user = users.find_one({"username":transaction['to_user'].lower()}, {'_id':1})

        del transaction['tid']
        del transaction['from_user']
        del transaction['to_user']

        if 'oid' in transaction:
            del transaction['oid']
        else:
            pass

        transaction['from_uid'] = str(from_user['_id'])
        transaction['to_uid'] = str(to_user['_id'])


        req_body = transaction
        headers = {'Content-type': 'application/json'}
        response, content = http.request(url, 'POST', headers=headers, body=json.dumps(req_body))
        print(content)
        time.sleep(1)

    print('########################## DONE!!!!!!! #####################')

if __name__ == '__main__':
    importUsers(users_data)
    importTransactions(transactions_data)
