import os
from eve import Eve
from flask import render_template
import jinja2



app = Eve(settings='settings.py')

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(os.getcwd()),
])

app.jinja_loader = my_loader

@app.route('/docs/api')
def index():
    return render_template('api.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
