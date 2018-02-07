from eve import Eve
app = Eve('API_VERSION':'v1')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
