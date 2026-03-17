# Potato Buyer Scraper

A modular, robots-aware scraper framework for collecting **public business leads** related to potato buyers in India.

## Features
- Weekly GitHub Actions workflow
- 60+ search queries from `config/queries.json`
- Site-specific adapters from `config/sites.json`
- Robots.txt checks before fetch
- Public email and phone extraction
- Deduplication and lead scoring
- CSV and JSON export
- Adapter review helper script

## Important
- Adapters are **disabled by default**
- Enable a site only after verifying:
  - robots.txt
  - terms of use
  - public page structure
  - selectors still work

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

## Output
- `output/india_potato_buyers.csv`
- `output/india_potato_buyers.json`
- `output/logs/scrape.log`

## GitHub Actions
The included workflow runs weekly and can also be triggered manually.
