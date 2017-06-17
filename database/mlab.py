import mongoengine

# mongodb://<dbuser>:<dbpassword>@ds129442.mlab.com:29442/hoocons
host = "ds129442.mlab.com"
port = 29442
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