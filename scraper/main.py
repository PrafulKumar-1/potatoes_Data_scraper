import logging
from typing import List
from urllib.parse import quote_plus

from bs4 import BeautifulSoup

from scraper.core.deduper import dedupe
from scraper.core.fetcher import Fetcher
from scraper.core.robots import RobotsPolicy
from scraper.core.utils import load_json
from scraper.models.adapter import SiteAdapter
from scraper.pipelines.export_pipeline import export_leads
from scraper.pipelines.profile_pipeline import scrape_profile
from scraper.pipelines.search_pipeline import collect_profile_links
from scraper.settings import (
    CSV_OUTPUT,
    JSON_OUTPUT,
    LOG_DIR,
    LOG_FILE,
    QUERIES_FILE,
    REQUEST_TIMEOUT,
    SITES_FILE,
    USER_AGENT,
)

HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-US,en;q=0.9",
}


def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def load_adapters() -> List[SiteAdapter]:
    raw = load_json(SITES_FILE)
    return [SiteAdapter(**item) for item in raw]


def scrape_adapter(adapter: SiteAdapter, queries: List[str], fetcher: Fetcher, robots_policy: RobotsPolicy):
    if not adapter.enabled:
        logging.info("[SKIP] %s disabled", adapter.name)
        return []

    all_leads = []
    seen_profiles = set()

    for keyword in queries:
        encoded = quote_plus(keyword)

        for template in adapter.search_urls:
            search_url = template.format(query=encoded)

            if not robots_policy.can_fetch(adapter.base_url, search_url):
                logging.warning("[BLOCKED] %s robots disallow %s", adapter.name, search_url)
                continue

            logging.info("[SEARCH] %s | %s", adapter.name, keyword)
            html = fetcher.fetch_html(search_url)
            if not html:
                continue

            soup = BeautifulSoup(html, "html.parser")
            profile_links = collect_profile_links(search_url, soup, adapter)

            if not profile_links:
                logging.info("[NO PROFILE LINKS] %s | %s", adapter.name, keyword)

            for profile_url in profile_links[: adapter.max_profiles_per_query]:
                if profile_url in seen_profiles:
                    continue
                seen_profiles.add(profile_url)

                leads = scrape_profile(adapter, profile_url, fetcher, robots_policy)
                if leads:
                    logging.info("[FOUND] %s -> %s leads", profile_url, len(leads))
                    all_leads.extend(leads)

    return dedupe(all_leads)


def main():
    setup_logging()
    fetcher = Fetcher(headers=HEADERS, timeout=REQUEST_TIMEOUT)
    robots_policy = RobotsPolicy(USER_AGENT)

    queries = load_json(QUERIES_FILE)
    adapters = load_adapters()

    all_leads = []
    for adapter in adapters:
        adapter_leads = scrape_adapter(adapter, queries, fetcher, robots_policy)
        logging.info("[ADAPTER DONE] %s -> %s leads", adapter.name, len(adapter_leads))
        all_leads.extend(adapter_leads)

    all_leads = dedupe(all_leads)

    # relaxed filter for debugging
    all_leads = [lead for lead in all_leads if lead.company_email]

    export_leads(all_leads, CSV_OUTPUT, JSON_OUTPUT)

    logging.info("Saved %s leads", len(all_leads))
    logging.info("CSV saved to: %s", CSV_OUTPUT.resolve())
    logging.info("JSON saved to: %s", JSON_OUTPUT.resolve())


if __name__ == "__main__":
    main()