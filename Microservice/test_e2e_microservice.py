import time
from threading import Thread

import pytest

from Microservice.utils import clear_db, put_item, view_items, send_item, update_item, view_sent_db

NAME = "A"
ADDRESS = "B"


def test_e2e_send_and_update():
    clear_db()
    put_item(NAME, ADDRESS)
    items = view_items()
    assert len(items) == 1, "Didn't add the item to the DB"
    items = view_items()
    id = next(iter(items))
    new_name = f"{NAME}newname"
    new_address = f"{ADDRESS}newaddress"

    thread1 = Thread(target=update_item, args=(id, new_name, new_address,))
    thread1.setDaemon(True)
    thread1.start()
    thread2 = Thread(target=send_item, args=(id,))
    thread2.setDaemon(True)
    thread2.start()
    thread1.join()
    thread2.join()

    # Check if it is deleted from the DB
    current_db = view_items()
    assert len(current_db) == 0, f"Didn't clear the DB, {current_db}"

    #Check if was sent to the right place
    sent_list = view_sent_db()
    assert sent_list['address'] == new_address , "Address didn't update when was sent"