from scraper.core.validators import is_public_business_email, profile_url_allowed

def test_is_public_business_email():
    assert is_public_business_email("hello@company.com")

def test_profile_url_allowed():
    assert profile_url_allowed(
        url="https://www.tradeindia.com/company/foo",
        base_url="https://www.tradeindia.com",
        must_contain=["/company/"],
    )
