from bs4 import BeautifulSoup

from scraper.core.extractor import clean_email, extract_company_name, extract_emails, extract_mailto_emails

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
