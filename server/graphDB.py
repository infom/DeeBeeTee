import os

from neomodel import (config, StructuredNode, StructuredRel, StringProperty, IntegerProperty, DateTimeProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom)

username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

config.DATABASE_URL = 'bolt://'+username+':'+password+'@194.87.236.140:7687'

class TransactionsRel(StructuredRel):
    since = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    tx = IntegerProperty()
'''
class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    balance = IntegerProperty(index=True, default=0)
    tx = RelationshipTo('Person', 'TX', model=TransactionsRel)
'''

class UserMixin(object):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    #balance = IntegerProperty(index=True, default=0)
    tx = RelationshipTo('Person', 'TX', model=TransactionsRel)

class BalanceMixin(object):
    credit_balance = IntegerProperty(index=True, default=0)
    debit_balance = IntegerProperty(index=True, default=0)
    balance = IntegerProperty(index=True, default=0)

    def credit_account(self, amount):
        self.credit_balance = self.credit_balance + int(amount)
        self.balance = self.balance + self.credit_balance
        self.save()

    def debit_account(self, amount):
        self.debit_balance = self.debit_balance + int(amount)
        self.balance = self.balance - self.debit_balance
        self.save()

class Person(StructuredNode, UserMixin, BalanceMixin):
    pass
