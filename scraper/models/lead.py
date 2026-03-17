from dataclasses import dataclass

@dataclass
class Lead:
    company_name: str
    company_email: str
    source_site: str
    source_url: str
    contact_page: str = ""
    phone: str = ""
    website: str = ""
    country_guess: str = ""
    buyer_signal: str = ""
