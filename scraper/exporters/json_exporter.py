import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from scraper.models.lead import Lead

def save_json(leads: Iterable[Lead], path: Path) -> None:
    leads = list(leads)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump([asdict(item) for item in leads], handle, ensure_ascii=False, indent=2)
