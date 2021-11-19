from typing import Callable, TypedDict

class Basevn(TypedDict):
    name: str
    get: Callable[[], list[dict]]
    transform: Callable[[list[dict]], list[dict]]
    schema: list[dict]
