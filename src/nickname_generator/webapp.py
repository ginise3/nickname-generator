"""Общий Streamlit UI, параметризуемый языком интерфейса.

Используется точками входа `app_ru.py` / `app_en.py` (и `app.py` как
дефолтным алиасом), чтобы не дублировать логику между локализованными
версиями приложения.
"""

from __future__ import annotations

import streamlit as st
import streamlit.components.v1 as components

from .clipboard import build_copy_list_html, build_single_copy_html
from .data import INVISIBLE_CHAR_ORDER, INVISIBLE_CHARS
from .generator import generate_nicknames
from .translations import STYLE_ORDER, TRANSLATIONS


def run_app(lang: str) -> None:
    """Рисует полное Streamlit-приложение на выбранном языке.

    Args:
        lang: код языка ("ru" или "en") — ключ в `TRANSLATIONS`.
    """
    t = TRANSLATIONS[lang]

    st.set_page_config(page_title=t["page_title"], page_icon=t["page_icon"], layout="centered")

    st.title(t["title"])
    st.caption(t["caption"])

    tab_generator, tab_invisible = st.tabs([t["tab_generator"], t["tab_invisible"]])

    # --- Вкладка 1: обычный генератор -------------------------------------

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
    with tab_generator:
        nicknames = st.session_state[state_key]
        if nicknames:
            st.subheader(res["subheader"])
            st.caption(res["copy_hint"])
            list_html, list_height = build_copy_list_html(
                nicknames,
                label=res["copy_button_label"],
                copied_label=res["copied_label"],
                failed_label=res["failed_label"],
            )
            components.html(list_html, height=list_height, scrolling=False)
        else:
            st.info(res["empty_info"])

    # --- Вкладка 2: невидимый ник ------------------------------------------

    inv = t["invisible"]
    with tab_invisible:
        st.subheader(inv["subheader"])
        st.write(inv["description"])

        preset_labels = {inv["presets"][key]: key for key in INVISIBLE_CHAR_ORDER}
        preset_choice = st.selectbox(inv["preset_label"], list(preset_labels.keys()))
        preset_key = preset_labels[preset_choice]
        invisible_char = INVISIBLE_CHARS[preset_key]

        repeat = st.slider(
            inv["repeat_label"],
            min_value=1,
            max_value=6,
            value=1,
            help=inv["repeat_help"],
        )
        invisible_nickname = invisible_char * repeat

        # Заметный сигнал о том, что результат только что пересчитался: тост при
        # реальном изменении параметров + всегда видимый зелёный success-блок.
        signature_key = f"invisible_signature_{lang}"
        signature = (preset_key, repeat)
        if signature_key in st.session_state and st.session_state[signature_key] != signature:
            st.toast(inv["updated_toast"], icon="🔄")
        st.session_state[signature_key] = signature

        st.success(inv["result_ready"].format(count=repeat, preset=preset_choice))

        st.write(inv["preview_label"])
        single_html, single_height = build_single_copy_html(
            invisible_nickname,
            label=inv["copy_button_label"],
            copied_label=inv["copied_label"],
            failed_label=inv["failed_label"],
        )
        components.html(single_html, height=single_height, scrolling=False)

        with st.expander(inv["how_to_header"]):
            st.markdown(inv["how_to_markdown"])
