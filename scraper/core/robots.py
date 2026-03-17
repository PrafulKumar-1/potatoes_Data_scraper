from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

class RobotsPolicy:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent
        self.cache = {}

    def can_fetch(self, base_url: str, url: str) -> bool:
        parsed = urlparse(base_url)
        root = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = root.rstrip("/") + "/robots.txt"

        if root not in self.cache:
            rp = RobotFileParser()
            rp.set_url(robots_url)
            try:
                rp.read()
                self.cache[root] = rp
            except Exception:
                self.cache[root] = None

        rp = self.cache[root]
        if rp is None:
            return False

        try:
            return rp.can_fetch(self.user_agent, url)
        except Exception:
            return False
