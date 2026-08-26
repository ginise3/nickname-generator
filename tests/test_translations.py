import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator.data import INVISIBLE_CHAR_ORDER, INVISIBLE_CHARS  # noqa: E402
from nickname_generator.translations import STYLE_ORDER, TRANSLATIONS  # noqa: E402


def test_all_languages_have_matching_style_keys():
    for lang, t in TRANSLATIONS.items():
        assert set(t["sidebar"]["style_options"].keys()) == set(STYLE_ORDER), lang


def test_all_languages_have_matching_invisible_preset_keys():
    for lang, t in TRANSLATIONS.items():
        presets = t["invisible"]["presets"]
        assert set(presets.keys()) == set(INVISIBLE_CHAR_ORDER) == set(INVISIBLE_CHARS.keys()), lang


def test_invisible_tab_has_required_strings():
    required_keys = (
        "copy_button_label",
        "copied_toast",
        "failed_toast",
        "updated_toast",
        "result_ready",
    )
    for lang, t in TRANSLATIONS.items():
        inv = t["invisible"]
        for key in required_keys:
            assert inv.get(key), f"missing/empty '{key}' for lang={lang}"


def test_result_ready_template_is_formattable():
    for lang, t in TRANSLATIONS.items():
        msg = t["invisible"]["result_ready"].format(count=3, preset="X")
        assert "{" not in msg and "}" not in msg, lang
