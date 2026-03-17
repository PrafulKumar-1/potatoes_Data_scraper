from scraper.core.robots import RobotsGroup, RobotsPolicy, RobotsRule


def test_robots_disallow_prefix_matches_query_string():
    groups = [
        RobotsGroup(
            user_agents=["*"],
            rules=[RobotsRule(directive="disallow", pattern="/search.php")],
        )
    ]
    assert not RobotsPolicy._can_fetch_with_groups(
        groups,
        "Mozilla/5.0 (compatible; PragmaBuyerCrawler/1.0)",
        "https://example.com/search.php?keyword=potato",
    )


def test_robots_disallow_wildcard_patterns():
    groups = [
        RobotsGroup(
            user_agents=["*"],
            rules=[RobotsRule(directive="disallow", pattern="*/search.html*")],
        )
    ]
    assert not RobotsPolicy._can_fetch_with_groups(
        groups,
        "Mozilla/5.0 (compatible; PragmaBuyerCrawler/1.0)",
        "https://example.com/catalog/search.html?keyword=potato",
    )


def test_robots_longest_match_prefers_allow():
    groups = [
        RobotsGroup(
            user_agents=["*"],
            rules=[
                RobotsRule(directive="disallow", pattern="/"),
                RobotsRule(directive="allow", pattern="/public/"),
            ],
        )
    ]
    assert RobotsPolicy._can_fetch_with_groups(
        groups,
        "Mozilla/5.0 (compatible; PragmaBuyerCrawler/1.0)",
        "https://example.com/public/listing",
    )


def test_parse_robots_keeps_rules_after_blank_line():
    groups = RobotsPolicy._parse_robots("User-agent: *\n\nDisallow: /search.php\n")
    assert len(groups) == 1
    assert groups[0].rules[0].pattern == "/search.php"
