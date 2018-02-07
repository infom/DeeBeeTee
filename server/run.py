from eve import Eve
from flask import render_template

app = Eve(settings='settings.py')

@app.route('/')
def index():
    return app.send_static_file('api.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
