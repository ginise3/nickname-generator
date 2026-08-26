"""Тесты для nickname_generator.clipboard (кнопки «Копировать» у списка ников).

Полноценная браузерная проверка (реальная запись в буфер обмена внутри
Streamlit-iframe + появление всплывающего тоста) выполняется вручную.
Здесь — статические проверки, фиксирующие регрессию конкретного бага:
копирование вызывало Clipboard API локального `window` внутри
сэндбоксированного iframe `components.html`, где браузер блокирует его
через Permissions Policy, поэтому кнопка «не копировала» ник.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator.clipboard import build_copy_list_html  # noqa: E402


def test_build_copy_list_html_returns_html_and_height():
    document, height = build_copy_list_html(["Alex", "Rogue_Wolf"])
    assert "Alex" in document
    assert "Rogue_Wolf" in document
    assert height > 0


def test_copy_uses_parent_window_clipboard_before_local():
    """Регрессия: копирование должно сначала пытаться писать в буфер обмена
    через `window.parent` (верхнеуровневый документ Streamlit-приложения,
    для которого Permissions Policy разрешает Clipboard API), а не только
    через локальный `navigator.clipboard` внутри iframe компонента.
    """
    document, _ = build_copy_list_html(["Alex"])
    assert "pw.navigator.clipboard.writeText" in document
    assert "navigator.clipboard.writeText" in document
    parent_pos = document.index("pw.navigator.clipboard.writeText")
    local_pos = document.index("navigator.clipboard.writeText")
    assert parent_pos < local_pos, "родительский Clipboard API должен пробоваться первым"


def test_copy_has_exec_command_fallback():
    document, _ = build_copy_list_html(["Alex"])
    assert 'execCommand("copy")' in document


def test_copy_shows_floating_toast_in_parent_document():
    """Всплывающая подсказка должна рисоваться в родительском документе
    (поверх всего приложения), а не быть обрезанной высотой iframe.
    """
    document, _ = build_copy_list_html(["Alex"])
    assert "nickname-copy-toast" in document
    assert "pw.document" in document


def test_toast_labels_are_localized():
    # json.dumps() экранирует не-ASCII в \uXXXX (валидно для JS, но не
    # совпадает с исходной строкой побайтово) — сравниваем с тем же
    # представлением, что уходит в HTML.
    document, _ = build_copy_list_html(
        ["Alex"], copied_label="Скопировано!", failed_label="Ошибка"
    )
    assert json.dumps("Скопировано!") in document
    assert json.dumps("Ошибка") in document
