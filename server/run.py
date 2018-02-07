from eve import Eve

app = Eve(settings='settings.py')

@app.route('/')
def index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
