from typing import Optional
import requests

class Fetcher:
    def __init__(self, headers: dict, timeout: int):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.timeout = timeout

    def fetch_html(self, url: str) -> Optional[str]:
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            if "text/html" not in response.headers.get("Content-Type", ""):
                return None
            return response.text
        except Exception:
            return None
