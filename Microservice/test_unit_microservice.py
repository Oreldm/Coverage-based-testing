import json

import pytest
import requests

from Microservice.utils import ADDRESS, clear_db, VIEWDB, put_item, view_items, send_item, update_item

NAME = "A"
ADDRESS = "B"

def test_put():
    clear_db()
    put_item(NAME, ADDRESS)
    items = view_items()
    assert len(items) == 1, "Didn't add the item to the DB"

def test_send():
    test_put()
    items = view_items()
    id = next(iter(items))
    send_item(id)
    items = view_items()
    assert len(items) == 0, "Didn't sent item"


def test_update():
    clear_db()
    test_put()
    items_before = view_items()
    id = next(iter(items_before))
    new_name = f"{NAME}newname"
    new_address = f"{ADDRESS}newaddress"
    update_item(id=id, name=f"{new_name}", address=f"{new_address}")
    items_after = view_items()
    after_name = items_after.get(id)['name']
    assert new_name == after_name, "Name is not as expected"
    after_address = items_after.get(id)['address']
    assert new_address == after_address, "Address is not as expected"
