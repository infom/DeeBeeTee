import os
import json
import jinja2

from eve import Eve
from eve_swagger import swagger, add_documentation
from router import *

app = Eve(settings='settings.py')
app.register_blueprint(swagger)

app.config['SWAGGER_INFO'] = {
    'title': 'DeeBeeTee API',
    'version': '1.0',
    'description': 'This is DeeBeeTee API Specification',
    'termsOfService': 'http://swagger.io/terms/',
    'contact': {
        'email': 'infominfom@gmail.com',
    },
    'license': {
        'name': 'Apache 2.0',
        'url': 'http://www.apache.org/licenses/LICENSE-2.0.html',
    },
    'schemes': ['http', 'https'],
}

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()+'/templates'),
])

app.jinja_loader = loader

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
