import os
from eve import Eve
from flask import render_template

app = Eve(settings='settings.py')

@app.route('/' methods=['GET'])
def index():
    path = os.path.abspath('api.html')
    return render_template(path)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
