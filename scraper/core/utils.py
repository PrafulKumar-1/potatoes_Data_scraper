import json
import random
import time
from pathlib import Path
from typing import Iterable, List

def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_text_lines(path: Path) -> List[str]:
    if not path.exists():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]

def sleep_jitter(min_s: float, max_s: float) -> None:
    if min_s < 0 or max_s < 0:
        return
    if max_s < min_s:
        min_s, max_s = max_s, min_s
    time.sleep(random.uniform(min_s, max_s))
