from bs4 import BeautifulSoup

from scraper.models.adapter import SiteAdapter
from scraper.pipelines.search_pipeline import collect_profile_links


def test_collect_profile_links_reads_json_script_urls():
    adapter = SiteAdapter(
        name="IndiaMART",
        base_url="https://www.indiamart.com",
        search_urls=["https://dir.indiamart.com/search.mp?ss={query}"],
        listing_link_selector="a[href]",
        company_name_selector="h2, h1",
        profile_url_must_contain=["/proddetail/", "/company/", "/seller/", "/impcat/"],
        profile_url_must_not_contain=["privacy"],
    )
    soup = BeautifulSoup(
        """
        <script id="__NEXT_DATA__" type="application/json">
        {
          "props": {
            "pageProps": {
              "searchResponse": {
                "results": [
                  {
                    "fields": {
                      "title_url": "https://www.indiamart.com/proddetail/test-123.html",
                      "url": "https://external.example.com/test"
                    }
                  }
                ]
              }
            }
          }
        }
        </script>
        """,
        "html.parser",
    )
    assert collect_profile_links("https://dir.indiamart.com/search.mp?ss=test", soup, adapter) == [
        "https://www.indiamart.com/proddetail/test-123.html"
    ]


def test_collect_profile_links_canonicalizes_tracking_query_params():
    adapter = SiteAdapter(
        name="IndiaMART",
        base_url="https://www.indiamart.com",
        search_urls=["https://dir.indiamart.com/search.mp?ss={query}"],
        listing_link_selector="a[href]",
        company_name_selector="h2, h1",
        profile_url_must_contain=["/proddetail/"],
        profile_url_must_not_contain=[],
    )
    soup = BeautifulSoup(
        """
        <a href="https://www.indiamart.com/proddetail/test-123.html?pos=1">First</a>
        <a href="https://www.indiamart.com/proddetail/test-123.html?pos=2">Second</a>
        """,
        "html.parser",
    )
    assert collect_profile_links("https://dir.indiamart.com/search.mp?ss=test", soup, adapter) == [
        "https://www.indiamart.com/proddetail/test-123.html"
    ]
