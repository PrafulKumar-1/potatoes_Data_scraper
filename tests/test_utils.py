from scraper.core.utils import load_text_lines
from pathlib import Path

def test_load_text_lines(tmp_path: Path):
    p = tmp_path / "x.txt"
    p.write_text("a\n\n b \n", encoding="utf-8")
    assert load_text_lines(p) == ["a", "b"]
