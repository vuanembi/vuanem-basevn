from dataclasses import dataclass
from typing import Callable


@dataclass
class Service:
    base_url: str
    token: str


@dataclass
class Resource:
    name: str
    get: Callable[[], list[dict]]
    transform: Callable[[list[dict]], list[dict]]
    schema: list[dict]
