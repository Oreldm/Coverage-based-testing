import json
import threading
import time

from flask import jsonify, current_app, request

from pyms.flask.app import Microservice

from Microservice.package import package
from Microservice.utils import PUT, VIEWSENT, VIEWDB, CLEARDB, SEND

ms1 = Microservice()
app1 = ms1.create_app()
packages = dict()
list = []


@app1.route("/")
def example():
    return jsonify({"main": "hello world {}".format(current_app.config["APP_NAME"])})


@app1.route(f"/cleardb")
def cleardb():
    """
    Usage: /cleardb
    """
    packages.clear()
    list.clear()
    return f"packages cleared"


@app1.route(f"/viewdb")
def viewdb():
    """
    Usage: /viewdb
    """
    return json.dumps(packages, indent=4)


@app1.route(f"/viewsent")
def viewsent():
    """
    Usage: /viewsent
    """
    return str(list)


@app1.route(f"/put")
def put_package():
    """
    Usage: /put?address=<?>&name=<?>
    id - optional
    """
    name = request.args.get('name')
    address = request.args.get('address')
    id = request.args.get('id')
    if id is None:
        p = package(name, address)
        packages[p.id] = {"name": p.name,
                          "address": p.address}
        return jsonify({"main": "got package"})
    else:
        packages.update({
            f"{id}": {
                "name": f"{name}",
                "address": f"{address}"
            }
        })
        return jsonify({"main": "updated package"})


@app1.route(f"/send")
def send_package():
    """
    Usage: /send?id=<?>
    """

    id = request.args.get('id')
    if id in packages:
        p = packages.pop(id)
        list.append({"id": id, "name": p['name'], "address": p['address']})
        return jsonify({"main": f"sent package {p['name']} to {p['address']} . ID: {id}"})
    return jsonify({"main": f"Didn't sent package {id}. Package does not exist"})


if __name__ == '__main__':
    threading.Thread(target=lambda: app1.run(port=5001)).start()
