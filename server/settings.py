MONGO_URI = "mongodb://remote:fgfHQ6PFzWNx@localhost:27017/deebeetee"

# включаем поддержку методов POST, PUT, PATCH, DELETE.
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

PUBLIC_METHODS = ['GET', 'POST']
PUBLIC_ITEM_METHODS = ['GET', 'POST']

API_VERSION = 'v1'

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

IF_MATCH = False

RENDERERS = ['eve.render.JSONRenderer']

users = {
    'schema': {
        'username': {
            'type': 'string',
            #'required': True,
            # уникальное поле (индекс не создаётся, просто значение должно быть уникальным)
            'unique': True,
        },
        'assign_date': {
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

transactions = {
    'schema': {
        'from_uid': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'field': '_id',
                'embeddable': True
            },
            'required': True,

        },
        'to_uid': {
            'type': 'objectid',
            'data_relation': {
                'resource': 'users',
                'field': '_id',
                'embeddable': True
            },
            'required': True,

        },
        'amount': {
            'type': 'integer',
            'required': True
        },
        'description': {
            'type': 'string',
        },
        'operation_date': {
            'type': 'datetime',
            'required': True,
        },
    }
}

DOMAIN = {'users':users, 'transactions':transactions}
