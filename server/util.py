def serializeDatetimeObjJSON(json):
    for key,val in json.items():
        if isinstance(val, datetime):
            json[key] = '{:%m/%d/%y %H:%M:%S}'.format(val) #you can add different formating here
            return json.dumps(json)
