"""Тесты для nickname_generator.webapp (общий Streamlit UI).

Полноценная браузерная проверка (Playwright, реальный DOM Streamlit-
приложения) подтвердила: сама кнопка копирования у st.code() имеет
собственный data-testid, но переключатель видимости (opacity: 0;
visibility: hidden по умолчанию) сидит на безымянных обёрточных <div> без
data-testid между `stCode` и `stElementToolbarButton`, у которых нестабильные
классы (`st-emotion-cache-*`). Здесь — статическая проверка, что CSS-
переопределение видимости кнопки копирования учитывает и эти обёртки (через
:has()), а не только саму кнопку, и использует `!important` (иначе его легко
перебивает встроенное правило Streamlit).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator.webapp import _ALWAYS_SHOW_COPY_BUTTON_CSS  # noqa: E402


def test_copy_button_css_targets_code_block_toolbar():
    css = _ALWAYS_SHOW_COPY_BUTTON_CSS
    assert 'data-testid="stCode"' in css
    assert 'data-testid="stElementToolbarButton"' in css


def test_copy_button_css_covers_unnamed_hover_wrapper_divs():
    """Регрессия: таргетить только саму кнопку недостаточно — реальный
    переключатель видимости сидит на её родительских <div> без data-testid.
    """
    css = _ALWAYS_SHOW_COPY_BUTTON_CSS
    assert ":has(" in css


def test_copy_button_css_forces_visibility_with_important():
    css = _ALWAYS_SHOW_COPY_BUTTON_CSS
    assert "opacity: 1 !important" in css
    assert "visibility: visible !important" in css


def test_copy_button_css_does_not_resize_the_icon():
    """Иконка должна остаться нативного размера — без transform/scale."""
    css = _ALWAYS_SHOW_COPY_BUTTON_CSS
    assert "scale(" not in css
    assert "transform" not in css
