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
    func = getattr(requests, request.method, None)
    if func is None:
        raise Exception(f"Invalid call method: {method}")
    last_called = time.time()
    rtn = func(**request.dict(exclude={"method"}))
    call_duration = time.time() - last_called
    call = {"time": last_called, "duration": call_duration, "response": rtn.json()}
    client.database["requestHistory"][hash_string].insert_one(call)