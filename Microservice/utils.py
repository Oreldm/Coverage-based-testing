import json

import requests

ADDRESS = "http://127.0.0.1"
ADDRESS_MS1 = f"{ADDRESS}:5001"
ADDRESS_MS2 = f"{ADDRESS}:5002"
CLEARDB = f"{ADDRESS_MS1}/cleardb"
VIEWDB = f"{ADDRESS_MS1}/viewdb"
VIEWSENT = f"{ADDRESS_MS1}/viewsent"
PUT = f"{ADDRESS_MS1}/put"
SEND = f"{ADDRESS_MS1}/send"
UPDATE = f"{ADDRESS_MS2}/update"

def view_items():
    res_str = requests.get(VIEWDB)
    res_dict = json.loads(res_str.text)
    return res_dict

def clear_db():
    requests.get(CLEARDB)
    current_db = view_items()
    assert len(current_db) == 0, "Didn't clear the DB"

def view_sent_db():
    res_str = requests.get(VIEWSENT)
    if res_str.text == '[]':
        return {}
    res_dict = json.loads(res_str.text.replace("[","").replace("]","").replace("\'", "\""))
    return res_dict


def put_item(name , address):
    requests.get(PUT, params={"name": f"{name}", "address": f"{address}"})

def send_item(id):
    current_db = view_items()
    requests.get(SEND, params={"id": f"{id}"})
    return current_db

def update_item(id, name, address):
    requests.get(UPDATE, params={"id": f"{id}",
                                 "name" : f"{name}",
                                 "address": f"{address}"
                                 } )

