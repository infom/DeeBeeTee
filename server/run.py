import os
from eve import Eve
from flask import render_template
import jinja2

app = Eve(settings='settings.py')

loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()),
])

app.jinja_loader = loader
app.config['UPLOAD_FOLDER'] =os.getcwd() + '/upload'

@app.route('/docs/api')
def api_docs():
    return render_template('docs/api/api.html')

@app.route('/graph')
def graph():
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'graphs.png')
    return render_template('templates/graph.html', image = full_filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
