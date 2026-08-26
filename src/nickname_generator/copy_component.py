"""Двунаправленная кнопка «Копировать» на чистом JS (без React/сборки).

В отличие от `clipboard.build_*_html` (одностороннее отображение через
`components.html`), этот компонент реализует минимальный протокол Streamlit
Components и умеет сообщать в Python, что копирование действительно
произошло — благодаря этому вызывающий код может показать настоящий
`st.toast(...)` сразу после клика.
"""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

import streamlit.components.v1 as components

_COMPONENT_DIR = Path(__file__).parent / "components" / "copy_button"
_copy_button_component = components.declare_component(
    "nickname_copy_button", path=str(_COMPONENT_DIR)
)


class CopyResult(TypedDict):
    """Результат последнего клика по кнопке копирования."""

    ok: bool
    ts: float
    text: str


def copy_button(text: str, label: str, key: str) -> CopyResult | None:
    """Рисует кнопку, которая копирует `text` в буфер обмена по клику.

    Возвращает `CopyResult` с результатом последнего клика (`ok` — удалось
    ли скопировать, `ts` — метка времени клика, чтобы отличать повторные
    клики с тем же текстом) или `None`, если кнопку ещё не нажимали.
    """
    return _copy_button_component(text=text, label=label, key=key, default=None)
