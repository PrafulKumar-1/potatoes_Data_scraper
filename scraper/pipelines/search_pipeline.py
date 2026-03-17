from typing import List

from scraper.core.parser import select_candidate_links
from scraper.core.validators import profile_url_allowed

def collect_profile_links(search_url: str, soup, adapter) -> List[str]:
    links = []
    for url in select_candidate_links(search_url, soup, adapter.listing_link_selector):
        if profile_url_allowed(
            url=url,
            base_url=adapter.base_url,
            must_contain=adapter.profile_url_must_contain,
            must_not_contain=adapter.profile_url_must_not_contain,
        ):
            links.append(url)
    return links
