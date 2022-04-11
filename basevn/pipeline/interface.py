from dataclasses import dataclass
from typing import Callable

import requests


@dataclass
class Service:
    base_url: str
    token: str


@dataclass
class Resource:
    name: str
    get: Callable[[requests.Session], list[dict]]
    transform: Callable[[list[dict]], list[dict]]
    schema: list[dict]
