import csv
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from scraper.models.lead import Lead

def save_csv(leads: Iterable[Lead], path: Path) -> None:
    leads = list(leads)
    fieldnames = [
        "company_name", "company_email", "source_site", "source_url",
        "contact_page", "phone", "website", "country_guess", "buyer_signal"
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for lead in leads:
            writer.writerow(asdict(lead))
