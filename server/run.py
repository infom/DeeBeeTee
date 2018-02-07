from eve import Eve
from eve.auth import requires_auth
app = Eve(settings='settings.py')

@app.route('/docs')
@requires_auth('resource')
def api_docs():
    return app.send_static_file('api.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
