from typing import List

from bs4 import BeautifulSoup

from scraper.core.extractor import (
    buyer_signal,
    extract_company_name,
    extract_external_website,
    guess_india,
)
from scraper.core.parser import text_content
from scraper.models.lead import Lead
from scraper.pipelines.contact_pipeline import collect_contact_data

def scrape_profile(adapter, profile_url, fetcher, robots_policy) -> List[Lead]:
    if not robots_policy.can_fetch(adapter.base_url, profile_url):
        return []

    html = fetcher.fetch_html(profile_url)
    if not html:
        return []

    soup = BeautifulSoup(html, "html.parser")
    company = extract_company_name(soup, adapter.company_name_selector)
    website = extract_external_website(profile_url, soup)

    pages, emails, phones = collect_contact_data(adapter, profile_url, soup, fetcher, robots_policy)
    combined_text = " ".join(text_content(page_soup) for _, page_soup in pages)

    country = "India" if guess_india(combined_text) else ""
    signal = buyer_signal(combined_text)
    contact_page = pages[1][0] if len(pages) > 1 else ""
    phone = next(iter(sorted(phones)), "")

    leads = []
    candidate_emails = sorted(emails) or [""]
    for email in candidate_emails:
        if not email and not any([company, phone, website]):
            continue
        leads.append(
            Lead(
                company_name=company,
                company_email=email,
                source_site=adapter.name,
                source_url=profile_url,
                contact_page=contact_page,
                phone=phone,
                website=website,
                country_guess=country,
                buyer_signal=signal,
            )
        )
    return leads
