import json
from datetime import datetime

def serializeDatetimeObjJSON(data):
    results = []
    for d in data:
        for key,val in d.items():
            if isinstance(val, datetime):
                d[key] = '{:%m/%d/%y %H:%M:%S}'.format(val) #you can add different formating here
        results.append(d)
        print(results)
    return json.dumps(results)


So this is embarrassing. I've got an application that I threw together in Flask and for now it is just serving up a single static HTML page with some links to CSS and JS. And I can't find where in the documentation Flask describes returning static files. Yes, I could use render_template but I know the data is not templatized. I'd have thought send_file or url_for was the right thing, but I could not get those to work. In the meantime, I am opening the files, reading content, and rigging up a Response with appropriate mimetype:

import os.path

from flask import Flask, Response


app = Flask(__name__)
app.config.from_object(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(root_dir, filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir, filename)
        # Figure out how flask returns static files
        # Tried:
        # - render_template
        # - send_file
        # This should not be so non-obvious
        return open(src).read()
    except IOError as exc:
        return str(exc)
