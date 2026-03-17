from typing import List, Tuple

from bs4 import BeautifulSoup

from scraper.core.extractor import contact_links, extract_emails, extract_mailto_emails, extract_phones
from scraper.core.parser import text_content, same_domain
from scraper.core.utils import sleep_jitter

def collect_contact_data(adapter, profile_url, soup, fetcher, robots_policy):
    pages = [(profile_url, soup)]
    emails = set(extract_emails(text_content(soup))) | extract_mailto_emails(soup)
    phones = set(extract_phones(text_content(soup)))

    for url in contact_links(profile_url, soup):
        if not same_domain(adapter.base_url, url):
            continue
        if not robots_policy.can_fetch(adapter.base_url, url):
            continue
        sleep_jitter(adapter.sleep_min, adapter.sleep_max)
        html = fetcher.fetch_html(url)
        if not html:
            continue
        contact_soup = BeautifulSoup(html, "html.parser")
        pages.append((url, contact_soup))
        emails |= extract_emails(text_content(contact_soup))
        emails |= extract_mailto_emails(contact_soup)
        phones |= extract_phones(text_content(contact_soup))

    return pages, emails, phones
