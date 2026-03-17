from typing import Optional
import requests

class Fetcher:
    def __init__(self, headers: dict, timeout: int):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.timeout = timeout
        self.last_status_code = None
        self.last_content_type = ""
        self.last_error = ""

    def fetch_html(self, url: str) -> Optional[str]:
        self.last_status_code = None
        self.last_content_type = ""
        self.last_error = ""
        try:
            response = self.session.get(url, timeout=self.timeout)
            self.last_status_code = response.status_code
            self.last_content_type = response.headers.get("Content-Type", "")
            response.raise_for_status()
            if "text/html" not in self.last_content_type:
                return None
            return response.text
        except requests.HTTPError as exc:
            if exc.response is not None:
                self.last_status_code = exc.response.status_code
                self.last_content_type = exc.response.headers.get("Content-Type", "")
            self.last_error = str(exc)
            return None
        except Exception as exc:
            self.last_error = str(exc)
            return None
