from __future__ import annotations

from collections.abc import MutableMapping
from dataclasses import dataclass, field
from typing import Optional, List
import pandas as pd
import requests
import time
import hashlib
import json

from qshed.client import QShedClient

client = QShedClient("http://localhost:5000")
db = client.database["requestHistory"]


@dataclass
class Request:
    url: str
    method: str = "get"
    headers: dict = field(default_factory=dict)
    data: dict = field(default_factory=dict)
    params: dict = field(default_factory=dict)
    last_called: Optional[float] = None

    def __post_init__(self) -> None:
        self._hash = self.__makehash()
        self._history_collection = db[self._hash]

    @staticmethod
    def __unique_string(url, method, params, headers, data):
        return json.dumps(
            {
                "url": url,
                "method": method,
                "params": params,
                "headers": headers,
                "data": data,
            }
        )

    @staticmethod
    def __hash_string(string) -> str:
        hash_obj = hashlib.sha256(bytes(string, "utf-8"))
        return hash_obj.hexdigest()

    def __makehash(self) -> str:
        attribs = ["url", "method", "params", "headers", "data"]
        string = self.__unique_string(
            **{attrib: getattr(self, attrib) for attrib in attribs}
        )
        return self.__hash_string(string)

    def add_history(self, call: dict) -> None:
        self._history_collection.insert_one(call)

    @classmethod
    def scheduler_call(cls, url, method="get", headers={}, data={}, params={}):
        hash_string = cls.__hash_string(
            cls.__unique_string(
                url=url, method=method, params=params, data=data, headers=headers
            )
        )
        # history_collection = db[hash_string]
        func = getattr(requests, method, None)
        if func is None:
            raise Exception(f"Invalid call method: {method}")
        last_called = time.time()
        rtn = func(url, params=params, headers=headers, data=data)
        call_duration = time.time() - last_called
        call = {"time": last_called, "duration": call_duration, "response": rtn.json()}
        db[hash_string].insert(call)
        print("done")

    def __call__(self) -> dict:
        func = getattr(requests, self.method, None)
        if func is None:
            raise Exception(f"Invalid call method: {self.method}")
        self.last_called = time.time()
        rtn = func(self.url, params=self.params, headers=self.headers, data=self.data)
        call_duration = time.time() - self.last_called
        call = {
            "time": self.last_called,
            "duration": call_duration,
            "response": rtn.json(),
        }
        self.add_history(call)
        return call
