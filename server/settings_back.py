MONGO_URI = "mongodb://remote:fgfHQ6PFzWNx@localhost:27017/deebeetee"

# включаем поддержку методов POST, PUT, PATCH, DELETE.
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

PUBLIC_METHODS = ['GET', 'POST']
PUBLIC_ITEM_METHODS = ['GET', 'POST']

API_VERSION = 'v1'

users = {
    # Здесь мы описываем модель данных. Для валидации используется модуль Cerberus от автора Eve.
    # Вы можете ознакомиться с ним в официальной документации модуля http://docs.python-cerberus.org/en/stable/.
    # Либо прочитать заметки в официальной документации EVE http://python-eve.org/validation.html#validation.
    'schema': {
        'username': {
            'type': 'string',
            'minlength': 5,
            'maxlength': 32,
            'required': True,
            # уникальное поле (индекс не создаётся, просто значение должно быть уникальным)
            'unique': True,
        },
        'firstname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 10,
            'required': True,
        },
        'lastname': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 15,
            'required': True,
        },
        'role': {
            'type': 'list', # тип: список
            'allowed': ["admin", "user"], # разрешаем использовать значения: "author", "contributor"
        },
        'location': {
            'type': 'dict', # тип: словарь
            # описываем "схему" словаря
            'schema': {
                'address': {'type': 'string'},
                'city': {'type': 'string'}
            },
        },
        'born': {
            'type': 'datetime',
        },
        'active': {
            'type': 'boolean',
            'default': True
        }
    }
}

groups = {
    # Описываем модель данных .
    'schema': {
        'title': {
            'type': 'string',
            'minlength': 5,
            'maxlength': 32,
            'required': True,
            'unique': True
        },
        'users': {
            'type': 'list',  # тип: список
            'default': [],   # по умолчанию: пустой список
            # описываем "схему" списка
            'schema': {
                'type': 'objectid', # тип данных: objectid
                # ссылаемся на запись в другой коллекции
                'data_relation': {
                    'resource': 'users',  # на ресурс `users` (который мы описали выше)
                    'field': '_id',  # на поле `_id`
                    'embeddable': True
                }
            }
        }
    }
}

DOMAIN = {'users':users, 'groups':groups}
