from eve import Eve
app = Eve(settings='settings.py')

@app.route('/docs')
def api_docs():
    return app.send_static_file('api.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
