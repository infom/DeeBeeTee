import json
from datetime import datetime

def serializeDatetimeObjJSON(data):
    for d in data:
        for key,val in d.items():
            if isinstance(val, datetime):
                d[key] = '{:%m/%d/%y %H:%M:%S}'.format(val) #you can add different formating here
                return json.dumps(d)
