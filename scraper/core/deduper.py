import re
from typing import Iterable, List, Tuple

from scraper.core.scorer import email_domain, quality_score
from scraper.models.lead import Lead

def normalize_company_name(name: str) -> str:
    value = (name or "").lower().strip()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    for token in ["private limited", "pvt ltd", "pvt", "ltd", "llp", "limited", "inc", "co", "company"]:
        value = value.replace(token, " ")
    value = re.sub(r"\s+", " ", value).strip()
    return value

def dedupe(leads: Iterable[Lead]) -> List[Lead]:
    best_by_key = {}
    for lead in leads:
        key_primary = (normalize_company_name(lead.company_name), email_domain(lead.company_email))
        key_fallback = (
            normalize_company_name(lead.company_name),
            lead.company_email.strip().lower(),
            lead.source_site.strip().lower(),
        )
        key = key_primary if key_primary[0] and key_primary[1] else key_fallback
        current = best_by_key.get(key)
        if current is None or quality_score(lead) > quality_score(current):
            best_by_key[key] = lead

    output = list(best_by_key.values())
    output.sort(key=quality_score, reverse=True)
    return output
