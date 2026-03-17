from scraper.main import build_search_jobs


def test_build_search_jobs_runs_static_templates_once():
    jobs = build_search_jobs(
        [
            "https://example.com/static.html",
            "https://example.com/search?q={query}",
        ],
        ["alpha", "beta"],
    )
    assert jobs == [
        ("[static]", "https://example.com/static.html"),
        ("alpha", "https://example.com/search?q=alpha"),
        ("beta", "https://example.com/search?q=beta"),
    ]
