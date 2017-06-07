import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds017544.mlab.com:17544/hoocons
host = "ds017544.mlab.com"
port = 17544
db_name = "hoocons"
username = "hoocon"
password = "1"


def connect():
    mongoengine.connect(db_name, host=host, port=port, username=username, password=password)


def list2json(l):
    import json
    return [json.loads(item.to_json()) for item in l]


def item2json(item):
    import json
    return json.loads(item.to_json())