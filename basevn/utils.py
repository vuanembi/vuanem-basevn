from typing import Any, Optional
import json
from datetime import datetime


def safe_string(x: Any) -> str:
    return json.dumps(x) if x else x


def parse_unix_ts(x: Optional[str]) -> Optional[str]:
    return datetime.fromtimestamp(int(x)).isoformat(timespec="seconds") if x else None
