import os
from eve import Eve
from flask import render_template
import jinja2

app = Eve(settings='settings.py')

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()+'/templates'),
])

app.jinja_loader = loader
app.config['STATIC_FOLDER'] = os.getcwd() + '/static'

@app.route('/docs/api')
def api_docs():
    return render_template('api.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
