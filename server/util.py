import os
import json
from datetime import datetime
from bson import ObjectId

def serializeJSON(data):
    results = []
    for d in data:
        for key,val in d.items():
            if isinstance(val, datetime):
                d[key] = '{:%m/%d/%y %H:%M:%S}'.format(val) #you can add different formating here
            if isinstance(val, ObjectId):
                d[kye] = str(val)
        results.append(d)
    return results

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
