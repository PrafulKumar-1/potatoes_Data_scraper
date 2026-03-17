from scraper.core.parser import normalize_url
from scraper.core.validators import profile_url_allowed


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

        if not profile_url_allowed(full, adapter.base_url, must_contain, must_not_contain):
            continue

        if full not in seen:
            seen.add(full)
            results.append(full)

    return results
