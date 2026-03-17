import re
from typing import Iterable, List, Optional, Set, Tuple
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from scraper.constants import BLOCKED_EMAIL_PARTS, CONTACT_HINTS, INDIA_HINTS
from scraper.core.parser import normalize_url, same_domain
from scraper.core.utils import load_text_lines
from scraper.settings import BLOCKED_DOMAINS_FILE

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[\s-]?)?(?:\(?\d{2,5}\)?[\s-]?)?[\d\s-]{6,15}\d")
BLOCKED_WEBSITE_DOMAINS = set(load_text_lines(BLOCKED_DOMAINS_FILE))
STRUCTURED_PHONE_PATTERNS = [
    re.compile(r'"(?:MOBILE_PNS|LANDLINE|pns|mobile)"\s*:\s*"([^"]+)"', re.IGNORECASE),
]

def clean_email(email: str) -> Optional[str]:
    email = email.strip().strip(".,;:()[]{}<>")
    lower = email.lower()
    if any(part in lower for part in BLOCKED_EMAIL_PARTS):
        return None
    return email

def extract_emails(text: str) -> Set[str]:
    found: Set[str] = set()
    for raw in EMAIL_RE.findall(text or ""):
        email = clean_email(raw)
        if email:
            found.add(email)
    return found

def extract_mailto_emails(soup: BeautifulSoup) -> Set[str]:
    found: Set[str] = set()
    for node in soup.select('a[href^="mailto:"]'):
        href = node.get("href", "")
        email = clean_email(href.replace("mailto:", "").split("?")[0])
        if email:
            found.add(email)
    return found

def extract_phones(text: str) -> Set[str]:
    found: Set[str] = set()
    for raw in PHONE_RE.findall(text or ""):
        phone = " ".join(raw.split())
        digits = re.sub(r"\D", "", phone)
        if len(digits) < 7 or len(digits) > 12:
            continue
        if re.fullmatch(r"\d{1,2}[-/]\d{1,2}[-/]\d{2,4}", phone):
            continue
        found.add(phone)
    return found


def extract_structured_phones(html: str) -> Set[str]:
    found: Set[str] = set()
    for pattern in STRUCTURED_PHONE_PATTERNS:
        for raw in pattern.findall(html or ""):
            found |= extract_phones(raw)
    return found

def guess_india(text: str) -> bool:
    lower = (text or "").lower()
    return any(hint in lower for hint in INDIA_HINTS)

def buyer_signal(text: str) -> str:
    lower = (text or "").lower()
    signals = []
    if "buyer" in lower or "importer" in lower:
        signals.append("buyer/importer")
    if "distributor" in lower or "wholesaler" in lower:
        signals.append("distributor/wholesaler")
    if any(word in lower for word in ["chips", "fries", "frozen", "starch"]):
        signals.append("potato-processor")
    return "; ".join(signals)

def extract_company_name(soup: BeautifulSoup, selectors: str) -> str:
    for selector in [s.strip() for s in selectors.split(",")]:
        node = soup.select_one(selector)
        if node:
            name = node.get_text(" ", strip=True)
            if name:
                return name[:200]
    if soup.title:
        return soup.title.get_text(" ", strip=True)[:200]
    return ""

def contact_links(page_url: str, soup: BeautifulSoup) -> List[str]:
    found = []
    seen = set()
    for node in soup.select("a[href]"):
        href = node.get("href")
        text = (node.get_text(" ", strip=True) or "").lower()
        full = normalize_url(page_url, href)
        if not full:
            continue
        lower_full = full.lower()
        if any(h in text for h in CONTACT_HINTS) or any(h in lower_full for h in CONTACT_HINTS):
            if full not in seen:
                seen.add(full)
                found.append(full)
    return found[:5]

def extract_external_website(page_url: str, soup: BeautifulSoup) -> str:
    fallback = ""
    for node in soup.select("a[href]"):
        href = node.get("href")
        full = normalize_url(page_url, href)
        if not full or same_domain(page_url, full):
            continue

        text = node.get_text(" ", strip=True).lower()
        lower_full = full.lower()
        hostname = urlparse(full).netloc.lower().replace("www.", "")
        if any(hostname == domain or hostname.endswith(f".{domain}") for domain in BLOCKED_WEBSITE_DOMAINS):
            continue

        if "google.com/maps" in lower_full or "get directions" in text or "direction" in text:
            continue

        if "website" in text or "website-link" in " ".join(node.get("class", [])):
            return full

        if not fallback:
            fallback = full
    return fallback
