import hashlib
from datetime import datetime


class package:
    def __init__(self, name, address):
        self.name = name
        self.address = address
        self.id = hashlib.sha256(f"{datetime.now()}{name}{address}".encode('utf-8')).hexdigest()