from eve import Eve
from  flask_bootstrap import Bootstrap
from eve_docs import eve_docs

app = Eve(settings='settings.py')

if __name__ == '__main__':
    Bootstrap(app)
    app.register_blueprint(eve_docs, url_prefix='/docs')
    app.run(host="0.0.0.0", port=5001, debug=True)
