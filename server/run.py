from eve import Eve
from flask import render_template

def get_cfg():
    cfg = {}
    base = home_link()['href']
    if '://' not in base:
        protocol = capp.config['PREFERRED_URL_SCHEME']
        print(base)
        base = '{0}://{1}'.format(protocol, base)

    cfg['base'] = base
    cfg['domains'] = {}
    cfg['server_name'] = capp.config['SERVER_NAME']
    cfg['api_name'] = capp.config.get('API_NAME', 'API')
    for domain, resource in list(capp.config['DOMAIN'].items()):
        if resource['item_methods'] or resource['resource_methods']:
            # hide the shadow collection for document versioning
            if 'VERSIONS' not in capp.config or not \
                    domain.endswith(capp.config['VERSIONS']):
                cfg['domains'][domain] = paths(domain, resource)
    return cfg

app = Eve(settings='settings.py')

@app.route('/docs')
def index():
    cfg = get_cfg()
    return render_template('api.html', cfg=cfg)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
