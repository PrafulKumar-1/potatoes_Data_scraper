from scraper.core.deduper import dedupe
from scraper.models.lead import Lead

def test_dedupe_keeps_best():
    a = Lead(company_name="Acme Pvt Ltd", company_email="sales@acme.com", source_site="A", source_url="https://a.com", country_guess="India")
    b = Lead(company_name="Acme Private Limited", company_email="sales@acme.com", source_site="B", source_url="https://b.com", country_guess="India", phone="+91 9999999999", website="https://acme.com", buyer_signal="buyer/importer")
    out = dedupe([a, b])
    assert len(out) == 1
    assert out[0].phone == "+91 9999999999"
