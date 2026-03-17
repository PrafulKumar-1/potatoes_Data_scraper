from bs4 import BeautifulSoup

from scraper.core.extractor import (
    clean_email,
    extract_company_name,
    extract_emails,
    extract_external_website,
    extract_mailto_emails,
    extract_phones,
)

def test_extract_emails():
    text = "Contact us at sales@example.org and info@test.co.in"
    emails = extract_emails(text)
    assert "sales@example.org" in emails
    assert "info@test.co.in" in emails

def test_clean_email_filters_images():
    assert clean_email("logo.png") is None

def test_extract_company_name():
    soup = BeautifulSoup("<html><h1>Acme Foods Pvt Ltd</h1></html>", "html.parser")
    assert extract_company_name(soup, "h1, h2") == "Acme Foods Pvt Ltd"

def test_extract_mailto_emails():
    soup = BeautifulSoup('<a href="mailto:hello@buyer.com">Mail</a>', "html.parser")
    assert "hello@buyer.com" in extract_mailto_emails(soup)


def test_extract_external_website_skips_blocked_domains():
    soup = BeautifulSoup(
        """
        <a href="https://facebook.com/acme">Facebook</a>
        <a href="https://acmefoods.in">Website</a>
        """,
        "html.parser",
    )
    assert extract_external_website("https://www.tradeindia.com/company/acme", soup) == "https://acmefoods.in"


def test_extract_phones_ignores_dates_and_long_ids():
    text = "GST Registration Date 27-03-2025 Product ID 2857729793573 Call +91 7943439804"
    phones = extract_phones(text)
    assert "+91 7943439804" in phones
    assert "27-03-2025" not in phones
    assert "2857729793573" not in phones


def test_extract_external_website_ignores_same_site_subdomains_and_maps():
    soup = BeautifulSoup(
        """
        <a href="https://my.indiamart.com/buyertools/postbl?modid=PRODDTL">Contact</a>
        <a href="https://www.google.com/maps/dir//13.057665,77.573898">Get Directions</a>
        <a class="website-link" href="https://www.neelakanthcargo.com/">Website</a>
        """,
        "html.parser",
    )
    assert extract_external_website(
        "https://www.indiamart.com/proddetail/test-123.html",
        soup,
    ) == "https://www.neelakanthcargo.com/"
