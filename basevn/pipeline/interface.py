from typing import Any
from dataclasses import dataclass
from typing import Callable

import requests

_GetFn = Callable[[dict[str, Any], int], list[dict]]
GetFn = Callable[[requests.Session], _GetFn]

@dataclass
class Service:
    base_url: str
    token: str


@dataclass
class Resource:
    name: str
    get: GetFn
    transform: Callable[[list[dict[str, Any]]], list[dict[str, Any]]]
    schema: list[dict[str, Any]]
