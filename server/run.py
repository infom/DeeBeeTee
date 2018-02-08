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
print(app.static_url_path)

@app.route('/docs/api')
def api_docs():
    return render_template('api.html')

@app.route('/graph')
def graph():
    return render_template('graph.html')

@app.route('/files/<path:filename>')
def files(filename):
    path = os.getcwd() + '/static/' + filename
    return app.send_from_directory(os.getcwd() + '/static/', filename, as_attachment=True)
    #return app.send_static_file(path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
