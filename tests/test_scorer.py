from scraper.core.scorer import quality_score
from scraper.models.lead import Lead

def test_quality_score_increases_with_data():
    basic = Lead(company_name="A", company_email="a@gmail.com", source_site="x", source_url="u")
    strong = Lead(company_name="A", company_email="a@company.com", source_site="x", source_url="u", phone="1234567", website="https://x.com", country_guess="India", buyer_signal="buyer/importer")
    assert quality_score(strong) > quality_score(basic)


def test_quality_score_treats_configured_free_domains_as_lower_quality():
    free = Lead(company_name="A", company_email="a@rediffmail.com", source_site="x", source_url="u")
    corporate = Lead(company_name="A", company_email="a@company.com", source_site="x", source_url="u")
    assert quality_score(corporate) > quality_score(free)
