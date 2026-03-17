import json

from scraper.core.utils import load_json
from scraper.settings import SITES_FILE

def adapter_review_checklist(adapter: dict) -> dict:
    return {
        "name": adapter["name"],
        "verify_robots_txt": True,
        "verify_terms": True,
        "verify_public_search_url": adapter["search_urls"][0] if adapter.get("search_urls") else "",
        "verify_profile_url_patterns": adapter.get("profile_url_must_contain", []),
        "verify_listing_link_selector": adapter.get("listing_link_selector", ""),
        "verify_company_name_selector": adapter.get("company_name_selector", ""),
        "enable_after_manual_review": False,
    }

def main():
    adapters = load_json(SITES_FILE)
    for adapter in adapters:
        print(json.dumps(adapter_review_checklist(adapter), ensure_ascii=False))

if __name__ == "__main__":
    main()
