from scraper.models.lead import Lead
from scraper.core.utils import load_text_lines
from scraper.settings import FREE_EMAIL_DOMAINS_FILE

FREE_WEBMAIL_DOMAINS = set(load_text_lines(FREE_EMAIL_DOMAINS_FILE)) or {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
}

def email_domain(email: str) -> str:
    return email.split("@", 1)[1].lower().strip() if "@" in email else ""

def quality_score(lead: Lead) -> int:
    score = 0
    if lead.company_email:
        score += 30
    if lead.phone:
        score += 10
    if lead.website:
        score += 10
    if lead.country_guess == "India":
        score += 20
    if lead.buyer_signal:
        score += 20
    domain = email_domain(lead.company_email)
    if domain and domain not in FREE_WEBMAIL_DOMAINS:
        score += 10
    return score
