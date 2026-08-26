"""Общий Streamlit UI, параметризуемый языком интерфейса.

Используется точками входа `app_ru.py` / `app_en.py` (и `app.py` как
дефолтным алиасом), чтобы не дублировать логику между локализованными
версиями приложения.
"""

from __future__ import annotations

import streamlit as st

from .generator import generate_nicknames
from .translations import STYLE_ORDER, TRANSLATIONS

# Кнопка/иконка копирования у st.code() встроена в Streamlit и по умолчанию
# показывается только при наведении курсора (opacity переключается на hover,
# CSS-классом или инлайн-стилем — в зависимости от версии). Раз ников в
# списке несколько и на мобильных устройствах наведения вообще нет, делаем
# её видимой всегда: переопределяем opacity/visibility с !important — это
# бьёт как CSS-правило Streamlit, так и возможный инлайн-стиль на hover.
# Заодно увеличиваем саму иконку (по умолчанию она мелкая) — масштабируем
# кнопку через transform, чтобы не ломать раскладку соседних элементов
# тулбара, и от правого верхнего угла (transform-origin), чтобы увеличенная
# иконка не съезжала за пределы блока кода.
# Селекторы намеренно избыточны (data-testid у разных версий Streamlit
# отличается: `stCode` — контейнер блока кода, `stElementToolbar*` — сама
# всплывающая панель с кнопкой) и ограничены только блоками `st.code()`,
# чтобы не трогать тулбары других виджетов (графиков, таблиц и т.д.).
_ALWAYS_SHOW_COPY_BUTTON_CSS = """
<style>
  div[data-testid="stCode"] [data-testid="stElementToolbar"],
  div[data-testid="stCode"] [data-testid="stElementToolbarButton"],
  div[data-testid="stCode"] [data-testid="stElementToolbarButtonContainer"],
  div[data-testid="stCode"] [data-testid="stElementToolbarButtonIcon"],
  div[data-testid="stCode"] button,
  div[data-testid="stCode"] [role="button"] {
    opacity: 1 !important;
    visibility: visible !important;
    pointer-events: auto !important;
  }
  div[data-testid="stCode"] [data-testid="stElementToolbarButton"],
  div[data-testid="stCode"] button {
    transform: scale(1.6);
    transform-origin: top right;
  }
  div[data-testid="stCode"] [data-testid="stElementToolbarButtonIcon"] svg {
    width: 1.3em !important;
    height: 1.3em !important;
  }
</style>
"""


def run_app(lang: str) -> None:
    """Рисует полное Streamlit-приложение на выбранном языке.

    Args:
        lang: код языка ("ru" или "en") — ключ в `TRANSLATIONS`.
    """
    t = TRANSLATIONS[lang]

    st.set_page_config(page_title=t["page_title"], page_icon=t["page_icon"], layout="centered")
    st.markdown(_ALWAYS_SHOW_COPY_BUTTON_CSS, unsafe_allow_html=True)

    st.title(t["title"])
    st.caption(t["caption"])

    sb = t["sidebar"]
    with st.sidebar:
        st.header(sb["header"])

        base_word = st.text_input(
            sb["base_word_label"],
            placeholder=sb["base_word_placeholder"],
        )

        style_labels = {sb["style_options"][style]: style for style in STYLE_ORDER}
        style_choice = st.selectbox(sb["style_label"], list(style_labels.keys()))

        count = st.slider(sb["count_label"], min_value=1, max_value=50, value=10)

        use_numbers = st.checkbox(sb["use_numbers_label"], value=True)
        use_leet = st.checkbox(sb["use_leet_label"], value=False)

        generate_clicked = st.button(sb["generate_button"], use_container_width=True)

    state_key = f"nicknames_{lang}"
    if state_key not in st.session_state:
        st.session_state[state_key] = []

    if generate_clicked:
        st.session_state[state_key] = generate_nicknames(
            base_word=base_word or None,
            style=style_labels[style_choice],
            count=count,
            use_numbers=use_numbers,
            use_leet=use_leet,
        )

    res = t["results"]
    nicknames = st.session_state[state_key]
    if nicknames:
        st.subheader(res["subheader"])
        st.caption(res["copy_hint"])
        # st.code() рисует нативный блок с собственной кнопкой копирования
        # в правом верхнем углу (всегда видимой — см. _ALWAYS_SHOW_COPY_-
        # BUTTON_CSS выше) — это встроенный механизм Streamlit, который
        # выполняется в основном окне страницы, а не в изолированном iframe,
        # поэтому его не блокирует политика безопасности браузера в
        # отношении Clipboard API.
        for nickname in nicknames:
            st.code(nickname, language=None)
    else:
        st.info(res["empty_info"])
