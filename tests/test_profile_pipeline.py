from scraper.models.adapter import SiteAdapter
from scraper.pipelines.profile_pipeline import scrape_profile


class DummyFetcher:
    def __init__(self, html_by_url):
        self.html_by_url = html_by_url

    def fetch_html(self, url):
        return self.html_by_url.get(url)


class AllowAllRobots:
    def can_fetch(self, base_url, url):
        return True


def test_scrape_profile_keeps_website_only_lead():
    adapter = SiteAdapter(
        name="IndiaMART",
        base_url="https://www.indiamart.com",
        search_urls=[],
        listing_link_selector="a[href]",
        company_name_selector="h2, h1",
    )
    profile_url = "https://www.indiamart.com/proddetail/test-123.html"
    html = """
    <html>
      <h2>Acme Foods Pvt Ltd</h2>
      <a href="https://acmefoods.in">Website</a>
    </html>
    """
    leads = scrape_profile(adapter, profile_url, DummyFetcher({profile_url: html}), AllowAllRobots())
    assert len(leads) == 1
    assert leads[0].company_name == "Acme Foods Pvt Ltd"
    assert leads[0].website == "https://acmefoods.in"
    assert leads[0].company_email == ""
