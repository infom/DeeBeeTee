MONGO_URI = "mongodb://remote:fgfHQ6PFzWNx@localhost:27017/deebeetee"

# включаем поддержку методов POST, PUT, PATCH, DELETE.
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

PUBLIC_METHODS = ['GET', 'POST']
PUBLIC_ITEM_METHODS = ['GET', 'POST']

API_VERSION = 'v1'

DATE_FORMAT = "%m/%d/%y %H:%M:%S"

IF_MATCH = False

RENDERERS = ['eve.render.JSONRenderer']

users = {
    'schema': {
        'uid': {
            'type' : 'integer',
            #S'required': True
        },
        'username': {
            'type': 'string',
            #'required': True,
            # уникальное поле (индекс не создаётся, просто значение должно быть уникальным)
            'unique': True,
        },
        'name':  {
            'type': 'string',
            #'required': True,
            # уникальное поле (индекс не создаётся, просто значение должно быть уникальным)
            #'unique': True,
        },
        'assing_date': {
            'type': 'datetime',
            #'required': True,
        },
        'user_id': {
            'type' : 'integer',
            #'required': True,
        }
    },

    'item_lookup_field':'username',

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,
    'item_url': 'regex("[\w,.:_-]+")'

}

getBalance = {
    'url': 'users/<regex("[\w,.:_-]+"):username>/getBalance'
}

transactions = {
    'schema': {
        'from_uid': {
            'type': 'integer',
            'required': True,
            'data_relation': {
                'resource': 'users',
                'field': 'uid',
                'embeddable': True
            },

        },
        'to_uid': {
            'type': 'integer',
            'required': True,
            'data_relation': {
                'resource': 'users',
                'field': 'uid',
                'embeddable': True
            },

        },
        'amount': {
            'type': 'integer',
            'required': True
        },
        'description': {
            'type': 'string',
        },
        'date': {
            'type': 'datetime',
            'required': True,
        },
    }
}

DOMAIN = {'users':users, 'transactions':transactions}
