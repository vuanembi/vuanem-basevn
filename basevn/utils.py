from typing import Any
import json


def safe_string(x: Any) -> str:
    return json.dumps(x) if x else x
