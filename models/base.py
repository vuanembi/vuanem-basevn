from typing import Callable, TypedDict
import json


class Basevn(TypedDict):
    name: str
    get: Callable[[], list[dict]]
    transform: Callable[[list[dict]], list[dict]]
    schema: list[dict]


def safe_string(x):
    return json.dumps(x) if isinstance(x, int) else x
