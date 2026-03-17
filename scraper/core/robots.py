import re
from dataclasses import dataclass
from typing import Dict, List, Optional
from urllib.parse import urlparse, urlsplit

import requests


@dataclass(frozen=True)
class RobotsRule:
    directive: str
    pattern: str


@dataclass(frozen=True)
class RobotsGroup:
    user_agents: List[str]
    rules: List[RobotsRule]


class RobotsPolicy:
    def __init__(self, user_agent: str, timeout: int = 20):
        self.user_agent = user_agent
        self.timeout = timeout
        self.cache: Dict[str, Optional[List[RobotsGroup]]] = {}

    @staticmethod
    def _root(base_url: str) -> str:
        parsed = urlparse(base_url)
        return f"{parsed.scheme}://{parsed.netloc}"

    @staticmethod
    def _path_with_query(url: str) -> str:
        parts = urlsplit(url)
        path = parts.path or "/"
        if parts.query:
            return f"{path}?{parts.query}"
        return path

    @staticmethod
    def _strip_comment(line: str) -> str:
        return line.split("#", 1)[0].strip()

    @classmethod
    def _parse_robots(cls, text: str) -> List[RobotsGroup]:
        groups: List[RobotsGroup] = []
        current_agents: List[str] = []
        current_rules: List[RobotsRule] = []

        def flush() -> None:
            nonlocal current_agents, current_rules
            if current_agents:
                groups.append(RobotsGroup(user_agents=current_agents, rules=current_rules))
            current_agents = []
            current_rules = []

        for raw_line in text.splitlines():
            line = cls._strip_comment(raw_line)
            if not line:
                continue

            if ":" not in line:
                continue

            key, value = [part.strip() for part in line.split(":", 1)]
            key = key.lower()
            value = value.strip()

            if key == "user-agent":
                if current_rules:
                    flush()
                current_agents.append(value.lower())
                continue

            if key in {"allow", "disallow"} and current_agents:
                current_rules.append(RobotsRule(directive=key, pattern=value))

        flush()
        return groups

    @staticmethod
    def _agent_match_length(user_agent: str, token: str) -> int:
        if token == "*":
            return 1
        if token and token in user_agent.lower():
            return len(token)
        return 0

    @staticmethod
    def _pattern_matches(pattern: str, path: str) -> bool:
        if not pattern:
            return False

        ends_with_anchor = pattern.endswith("$")
        pattern = pattern[:-1] if ends_with_anchor else pattern

        escaped = []
        for char in pattern:
            if char == "*":
                escaped.append(".*")
            else:
                escaped.append(re.escape(char))

        regex = "^" + "".join(escaped)
        if ends_with_anchor:
            regex += "$"
        return re.match(regex, path) is not None

    @classmethod
    def _can_fetch_with_groups(cls, groups: List[RobotsGroup], user_agent: str, url: str) -> bool:
        path = cls._path_with_query(url)
        best_match = 0
        applicable_rules: List[RobotsRule] = []

        for group in groups:
            match_length = max((cls._agent_match_length(user_agent, token) for token in group.user_agents), default=0)
            if match_length == 0:
                continue
            if match_length > best_match:
                best_match = match_length
                applicable_rules = list(group.rules)
            elif match_length == best_match:
                applicable_rules.extend(group.rules)

        if not applicable_rules:
            return True

        winning_rule: Optional[RobotsRule] = None
        winning_length = -1
        for rule in applicable_rules:
            if not cls._pattern_matches(rule.pattern, path):
                continue

            normalized_pattern = rule.pattern.rstrip("$")
            pattern_length = len(normalized_pattern.replace("*", ""))
            if pattern_length > winning_length:
                winning_rule = rule
                winning_length = pattern_length
            elif pattern_length == winning_length and winning_rule and winning_rule.directive == "disallow" and rule.directive == "allow":
                winning_rule = rule

        if winning_rule is None:
            return True
        return winning_rule.directive != "disallow"

    def _fetch_groups(self, root: str) -> Optional[List[RobotsGroup]]:
        robots_url = root.rstrip("/") + "/robots.txt"
        try:
            response = requests.get(
                robots_url,
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent},
            )
            response.raise_for_status()
        except Exception:
            return None
        return self._parse_robots(response.text)

    def can_fetch(self, base_url: str, url: str) -> bool:
        root = self._root(url or base_url)
        if root not in self.cache:
            self.cache[root] = self._fetch_groups(root)

        groups = self.cache[root]
        if groups is None:
            return False

        try:
            return self._can_fetch_with_groups(groups, self.user_agent, url)
        except Exception:
            return False
