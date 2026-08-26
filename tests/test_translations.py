import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator.translations import STYLE_ORDER, TRANSLATIONS  # noqa: E402


def test_all_languages_have_matching_style_keys():
    for lang, t in TRANSLATIONS.items():
        assert set(t["sidebar"]["style_options"].keys()) == set(STYLE_ORDER), lang
