from scraper.core.parser import same_domain

def profile_url_allowed(url: str, base_url: str, must_contain=None, must_not_contain=None) -> bool:
    if not same_domain(url, base_url):
        return False
    lower = url.lower()
    if must_not_contain and any(part in lower for part in must_not_contain):
        return False
    if must_contain and not any(part in lower for part in must_contain):
        return False
    return True

def is_public_business_email(email: str) -> bool:
    return "@" in email and len(email) >= 6
