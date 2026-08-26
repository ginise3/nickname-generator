import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator import generate_nicknames
from nickname_generator.generator import Style


def test_generate_default_count():
    nicknames = generate_nicknames(count=5)
    assert len(nicknames) == 5
    assert len(set(nicknames)) == len(nicknames)


def test_generate_zero_count():
    assert generate_nicknames(count=0) == []


def test_generate_with_base_word():
    nicknames = generate_nicknames(base_word="alex", style=Style.GAMER, count=3)
    assert len(nicknames) == 3
    for nickname in nicknames:
        assert "Alex" in nickname


def test_generate_with_numbers():
    nicknames = generate_nicknames(count=3, use_numbers=True)
    for nickname in nicknames:
        assert any(ch.isdigit() for ch in nickname)


def test_generate_with_leet():
    nicknames = generate_nicknames(base_word="test", count=3, use_leet=True)
    for nickname in nicknames:
        assert "7357" in nickname.replace("-", "").replace("_", "").replace(".", "")
