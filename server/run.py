from eve import Eve
from flask import render_template

app = Eve(settings='settings.py')

@app.route('/')
def index():
    return render_template("api.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
