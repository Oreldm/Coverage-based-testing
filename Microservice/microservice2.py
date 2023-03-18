import json
import threading
import time

import requests
from flask import jsonify, current_app, request

from pyms.flask.app import Microservice

from Microservice.package import package
from Microservice.utils import view_items, SEND, PUT, UPDATE

ms2 = Microservice()
app2 = ms2.create_app()
packages = dict()
list = []



@app2.route(f"/update")
def update_addr():
    """
    Usage: /update?id=<?>&address=<?>&name=<?>
    """
    time.sleep(5)
    id = request.args.get('id')
    address = request.args.get('address')
    name = request.args.get('name')
    current_db = view_items()

    if id in current_db:
        requests.get(PUT, {"id": f"{id}",
                                 "name" : f"{name}",
                                 "address": f"{address}"
                                 })
        return jsonify({"main": f"update package {id}"})
    return jsonify({"main": f"Didn't update package {id}. Package does not exist"})


if __name__ == '__main__':
    threading.Thread(target=lambda: app2.run(port=5002)).start()
