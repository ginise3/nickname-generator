import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator.translations import STYLE_ORDER, TRANSLATIONS  # noqa: E402


def test_all_languages_have_matching_style_keys():
    for lang, t in TRANSLATIONS.items():
        assert set(t["sidebar"]["style_options"].keys()) == set(STYLE_ORDER), lang


def test_all_languages_have_required_results_strings():
    required_keys = ("subheader", "copy_hint", "empty_info")
    for lang, t in TRANSLATIONS.items():
        res = t["results"]
        for key in required_keys:
            assert res.get(key), f"missing/empty '{key}' for lang={lang}"
