from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT_DIR / "config"
OUTPUT_DIR = ROOT_DIR / "output"
LOG_DIR = OUTPUT_DIR / "logs"

QUERIES_FILE = CONFIG_DIR / "queries.json"
SITES_FILE = CONFIG_DIR / "sites.json"
BLOCKED_DOMAINS_FILE = CONFIG_DIR / "blocked_domains.txt"
FREE_EMAIL_DOMAINS_FILE = CONFIG_DIR / "free_email_domains.txt"

CSV_OUTPUT = OUTPUT_DIR / "india_potato_buyers.csv"
JSON_OUTPUT = OUTPUT_DIR / "india_potato_buyers.json"
LOG_FILE = LOG_DIR / "scrape.log"

USER_AGENT = "Mozilla/5.0 (compatible; PragmaBuyerCrawler/1.0; +https://example.com/bot)"
REQUEST_TIMEOUT = 20
DEFAULT_SLEEP_MIN = 1.5
DEFAULT_SLEEP_MAX = 3.0
