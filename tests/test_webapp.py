"""Тесты для nickname_generator.webapp (общий Streamlit UI).

Полноценная браузерная проверка (что иконка копирования у st.code()
действительно видна без наведения курсора и увеличена) выполняется вручную.
Здесь — статическая проверка, что CSS-переопределение видимости и размера
кнопки копирования присутствует, покрывает нужные data-testid и использует
`!important` там, где это нужно (иначе его легко перебивает встроенный
hover-стиль Streamlit).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator.webapp import _ALWAYS_SHOW_COPY_BUTTON_CSS  # noqa: E402


def test_copy_button_css_targets_code_block_toolbar():
    css = _ALWAYS_SHOW_COPY_BUTTON_CSS
    assert 'data-testid="stCode"' in css
    assert 'data-testid="stElementToolbar"' in css


def test_copy_button_css_forces_visibility_with_important():
    css = _ALWAYS_SHOW_COPY_BUTTON_CSS
    assert "opacity: 1 !important" in css
    assert "visibility: visible !important" in css


def test_copy_button_css_enlarges_the_icon():
    css = _ALWAYS_SHOW_COPY_BUTTON_CSS
    assert "transform: scale(" in css
    assert "transform-origin: top right" in css
