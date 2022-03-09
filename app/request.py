from flask import current_app

import requests
import time
import hashlib
import json

from app import client


def string_hash(string) -> str:
    hash_obj = hashlib.sha256(bytes(string, "utf-8"))
    return hash_obj.hexdigest()

def call_request(request):
    hash_string = string_hash(request.json())
    func = getattr(requests, method, None)
    if func is None:
        raise Exception(f"Invalid call method: {method}")
    last_called = time.time()
    rtn = func(**request.dict())
    call_duration = time.time() - last_called
    call = {"time": last_called, "duration": call_duration, "response": rtn.json()}
    client.database[current_app.config["REQUEST_DATABASE"]][hash_string].insert(call)
    print("done")