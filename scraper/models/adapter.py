from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class SiteAdapter:
    name: str
    base_url: str
    search_urls: List[str]
    listing_link_selector: str
    company_name_selector: str
    enabled: bool = False
    sleep_min: float = 1.5
    sleep_max: float = 3.0
    max_search_pages: int = 2
    max_profiles_per_query: int = 25
    profile_url_must_contain: Optional[List[str]] = None
    profile_url_must_not_contain: Optional[List[str]] = None
