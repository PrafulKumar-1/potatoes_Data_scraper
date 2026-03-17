import json
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from scraper.settings import QUERIES_FILE

def main():
    queries = json.loads(QUERIES_FILE.read_text(encoding="utf-8"))
    for idx, query in enumerate(queries, start=1):
        print(f"{idx:02d}. {query}")

if __name__ == "__main__":
    main()
