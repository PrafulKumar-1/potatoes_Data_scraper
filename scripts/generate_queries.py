import json
from pathlib import Path

from scraper.settings import QUERIES_FILE

def main():
    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))
    for idx, query in enumerate(queries, start=1):
        print(f"{idx:02d}. {query}")

if __name__ == "__main__":
    main()
