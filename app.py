"""Streamlit-приложение: генератор ников."""

from __future__ import annotations

import sys
from pathlib import Path

# Позволяет запускать `streamlit run app.py` без предварительной установки пакета.
sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st
import streamlit.components.v1 as components

from nickname_generator import generate_nicknames
from nickname_generator.clipboard import build_copy_list_html, build_single_copy_html
from nickname_generator.data import INVISIBLE_CHARS
from nickname_generator.generator import Style

st.set_page_config(page_title="Генератор ников", page_icon="🎮", layout="centered")

st.title("🎮 Генератор ников")
st.caption("Придумай уникальный ник для игр, соцсетей и не только")

tab_generator, tab_invisible = st.tabs(["🎲 Генератор ников", "👻 Невидимый ник"])

# --- Вкладка 1: обычный генератор -------------------------------------------------

with st.sidebar:
    st.header("Настройки")

    base_word = st.text_input(
        "Слово или имя для основы ника (необязательно)",
        placeholder="например, Alex",
    )

    style_labels = {
        "Случайный": Style.RANDOM,
        "Геймерский": Style.GAMER,
        "Милый": Style.CUTE,
    }
    style_choice = st.selectbox("Стиль", list(style_labels.keys()))

    count = st.slider("Количество ников", min_value=1, max_value=50, value=10)

    use_numbers = st.checkbox("Добавлять числа", value=True)
    use_leet = st.checkbox("Leet-speak (а → 4, о → 0 и т.д.)", value=False)

    generate_clicked = st.button("✨ Сгенерировать", use_container_width=True)

if "nicknames" not in st.session_state:
    st.session_state.nicknames = []

if generate_clicked:
    st.session_state.nicknames = generate_nicknames(
        base_word=base_word or None,
        style=style_labels[style_choice],
        count=count,
        use_numbers=use_numbers,
        use_leet=use_leet,
    )

with tab_generator:
    if st.session_state.nicknames:
        st.subheader("Результат")
        st.caption("Нажми «Копировать» рядом с ником, чтобы скопировать его в буфер обмена.")
        list_html, list_height = build_copy_list_html(st.session_state.nicknames)
        components.html(list_html, height=list_height, scrolling=False)
    else:
        st.info("Настрой параметры слева и нажми «Сгенерировать».")

# --- Вкладка 2: невидимый ник -------------------------------------------------

with tab_invisible:
    st.subheader("Невидимый ник")
    st.write(
        "Некоторые Unicode-символы выглядят как пустота, но не являются обычным "
        "пробелом — Discord, Telegram и многие игры принимают их как имя, "
        "хотя визуально ник кажется пустым."
    )

    preset_name = st.selectbox("Платформа / вариант символа", list(INVISIBLE_CHARS.keys()))
    invisible_char = INVISIBLE_CHARS[preset_name]

    repeat = st.slider(
        "Сколько символов использовать",
        min_value=1,
        max_value=6,
        value=1,
        help="Некоторые платформы требуют минимум 2 символа для имени.",
    )
    invisible_nickname = invisible_char * repeat

    st.write("Твой невидимый ник (выглядит пустым, но содержит символ):")
    single_html, single_height = build_single_copy_html(invisible_nickname, "📋 Копировать невидимый ник")
    components.html(single_html, height=single_height, scrolling=False)

    with st.expander("Как использовать"):
        st.markdown(
            """
1. Нажми **«Копировать невидимый ник»** выше.
2. Открой настройки профиля/ника в Discord, Telegram или игре.
3. Вставь скопированный символ в поле имени (`Ctrl+V` / `⌘+V`).
4. Если платформа не принимает ник (пишет «имя пустое» или «слишком короткое»),
   увеличь количество символов ползунком выше или попробуй другой вариант из списка —
   разные платформы по-разному фильтруют "пустые" символы.
5. Сохрани изменения.

**Подсказка:** для Discord обычно лучше подходит *Braille Pattern Blank* (⠀),
для Telegram — *Hangul Filler* (ㅤ). *Zero-Width Space* удобно комбинировать
с другими символами, если нужен ник длиннее одного символа.
            """
        )
