"""Тесты для двунаправленной кнопки копирования (nickname_generator.copy_component).

Полноценная браузерная проверка (реальная запись в буфер обмена + появление
st.toast) была выполнена вручную через Playwright/Chromium в ходе разработки
и подтвердила, что компонент работает как задумано. Здесь — лёгкие
статические проверки, которые не тянут Playwright/Chromium в зависимости
проекта, но фиксируют регрессию конкретного бага, из-за которого кнопка не
работала (см. ниже).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nickname_generator.copy_component import copy_button  # noqa: E402

_COMPONENT_HTML = (
    Path(__file__).parent.parent
    / "src"
    / "nickname_generator"
    / "components"
    / "copy_button"
    / "index.html"
).read_text(encoding="utf-8")


def test_copy_button_is_callable():
    assert callable(copy_button)


def test_render_listener_does_not_require_is_streamlit_message():
    """Регрессия: Streamlit отправляет сообщение "streamlit:render" БЕЗ поля
    isStreamlitMessage (эта метка есть только на сообщениях от компонента
    К Streamlit, не наоборот). Фильтрация входящих сообщений по этому полю
    тихо роняла render — кнопка оставалась без текста, iframe не менял
    высоту, клики не долетали до JS-обработчика.
    """
    match = re.search(r'addEventListener\("message".*?\}\);', _COMPONENT_HTML, re.DOTALL)
    assert match, "не найден обработчик window.addEventListener('message', ...)"
    handler_code = match.group(0)
    assert "streamlit:render" in handler_code
    assert "isStreamlitMessage" not in handler_code


def test_component_sends_required_outbound_messages():
    assert "streamlit:componentReady" in _COMPONENT_HTML
    assert "streamlit:setComponentValue" in _COMPONENT_HTML
    assert "streamlit:setFrameHeight" in _COMPONENT_HTML
    assert "apiVersion" in _COMPONENT_HTML


def test_component_writes_clipboard_with_fallback():
    assert "navigator.clipboard" in _COMPONENT_HTML
    assert 'execCommand("copy")' in _COMPONENT_HTML
