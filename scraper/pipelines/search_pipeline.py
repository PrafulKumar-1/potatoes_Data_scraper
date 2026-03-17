import json
from urllib.parse import urlsplit, urlunsplit

from scraper.core.parser import normalize_url
from scraper.core.validators import profile_url_allowed


def canonical_profile_url(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def collect_json_profile_links(current_url, soup, adapter, must_contain, must_not_contain):
    results = []
    seen = set()

    def visit(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if isinstance(value, str) and "url" in key.lower():
                    full = normalize_url(current_url, value)
                    if full:
                        full = canonical_profile_url(full)
                    if full and profile_url_allowed(full, adapter.base_url, must_contain, must_not_contain):
                        if full not in seen:
                            seen.add(full)
                            results.append(full)
                elif isinstance(value, (dict, list)):
                    visit(value)
        elif isinstance(node, list):
            for item in node:
                if isinstance(item, (dict, list)):
                    visit(item)

    for script in soup.select('script[type="application/json"]'):
        text = script.get_text(strip=True)
        if not text:
            continue
        try:
            visit(json.loads(text))
        except json.JSONDecodeError:
            continue

    return results


def collect_profile_links(current_url, soup, adapter):
    results = []
    seen = set()

    must_contain = [x.lower() for x in (adapter.profile_url_must_contain or [])]
    must_not_contain = [x.lower() for x in (adapter.profile_url_must_not_contain or [])]

    for a in soup.select(adapter.listing_link_selector):
        href = a.get("href")
        full = normalize_url(current_url, href)
        if full:
            full = canonical_profile_url(full)
        if not full:
            continue

        if not profile_url_allowed(full, adapter.base_url, must_contain, must_not_contain):
            continue

        if full not in seen:
            seen.add(full)
            results.append(full)

    if results:
        return results

    return collect_json_profile_links(current_url, soup, adapter, must_contain, must_not_contain)
