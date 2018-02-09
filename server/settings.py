MONGO_URI = "mongodb://remote:fgfHQ6PFzWNx@localhost:27017/deebeetee"

# включаем поддержку методов POST, PUT, PATCH, DELETE.
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

PUBLIC_METHODS = ['GET', 'POST']
PUBLIC_ITEM_METHODS = ['GET', 'POST']

API_VERSION = 'v1'

DATE_FORMAT = "%m/%d/%y %H:%M:%S"

IF_MATCH = False

users = {
    'schema': {
        'uid': {
            'type' : 'integer',
            'required': True
        },
        'username': {
            'type': 'string',
            'required': True,
            # уникальное поле (индекс не создаётся, просто значение должно быть уникальным)
            'unique': True,
        },
        'name':  {
            'type': 'string',
            'required': True,
            # уникальное поле (индекс не создаётся, просто значение должно быть уникальным)
            #'unique': True,
        },
        'assing_date': {
            'type': 'datetime',
            'required': True,
        },
        'user_id': {
            'type' : 'integer',
            'required': True,
        }
    },

    'additional_lookup': {
        'url': 'regex("[\w]+")',
        'field': 'username',
    },

    # We also disable endpoint caching as we don't want client apps to
    # cache account data.
    'cache_control': '',
    'cache_expires': 0,
}

DOMAIN = {'users':users}
