import os

from neomodel import (config, StructuredNode, StructuredRel, StringProperty, IntegerProperty, DateTimeProperty,
    UniqueIdProperty, RelationshipTo, RelationshipFrom)

username = os.environ.get('NEO4J_USERNAME')
password = os.environ.get('NEO4J_PASSWORD')

config.DATABASE_URL = 'bolt://'+username+':'+password+'@194.87.236.140:7687'

class TransactionsRel(StructuredRel):
    since = DateTimeProperty(default=lambda: datetime.now(pytz.utc))
    tx = IntegerProperty()

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    balance = IntegerProperty(index=True, default=0)
    tx = RelationshipTo('Person', 'TX', model=TransactionsRel)
