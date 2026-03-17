from urllib.parse import urljoin, urlparse


def normalize_url(base_url: str, href: str):
    if not href:
        return None
    if href.startswith("javascript:") or href.startswith("mailto:") or href.startswith("tel:"):
        return None
    return urljoin(base_url, href)


def same_domain(a: str, b: str) -> bool:
    da = urlparse(a).netloc.replace("www.", "")
    db = urlparse(b).netloc.replace("www.", "")
    return da == db


def collect_profile_links(current_url, soup, adapter):
    results = []
    seen = set()

    must_contain = [x.lower() for x in (adapter.profile_url_must_contain or [])]
    must_not_contain = [x.lower() for x in (adapter.profile_url_must_not_contain or [])]

    for a in soup.select(adapter.listing_link_selector):
        href = a.get("href")
        full = normalize_url(current_url, href)
        if not full:
            continue

        if not same_domain(adapter.base_url, full):
            continue

        lo = full.lower()

        if any(x in lo for x in must_not_contain):
            continue

        if must_contain and not any(x in lo for x in must_contain):
            continue

        if full not in seen:
            seen.add(full)
            results.append(full)

    return results