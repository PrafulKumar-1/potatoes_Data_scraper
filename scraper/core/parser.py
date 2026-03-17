from typing import List, Optional
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

def soup_from_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "html.parser")

def normalize_url(base_url: str, href: Optional[str]) -> Optional[str]:
    if not href:
        return None
    if href.startswith(("javascript:", "mailto:", "tel:")):
        return None
    return urljoin(base_url, href)

def same_domain(a: str, b: str) -> bool:
    da = urlparse(a).netloc.lower().split(":", 1)[0].replace("www.", "")
    db = urlparse(b).netloc.lower().split(":", 1)[0].replace("www.", "")
    return da == db or da.endswith(f".{db}") or db.endswith(f".{da}")

def text_content(soup: BeautifulSoup) -> str:
    return soup.get_text(" ", strip=True)

def select_candidate_links(current_url: str, soup: BeautifulSoup, listing_selector: str) -> List[str]:
    out = []
    seen = set()
    for node in soup.select(listing_selector):
        href = node.get("href")
        full = normalize_url(current_url, href)
        if full and full not in seen:
            seen.add(full)
            out.append(full)
    return out
