"""Streamlit-приложение: генератор ников."""

from __future__ import annotations

import sys
from pathlib import Path

# Позволяет запускать `streamlit run app.py` без предварительной установки пакета.
sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st

from nickname_generator import generate_nicknames
from nickname_generator.generator import Style

st.set_page_config(page_title="Генератор ников", page_icon="🎮", layout="centered")

st.title("🎮 Генератор ников")
st.caption("Придумай уникальный ник для игр, соцсетей и не только")

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

if st.session_state.nicknames:
    st.subheader("Результат")
    for nickname in st.session_state.nicknames:
        st.code(nickname, language=None)
else:
    st.info("Настрой параметры слева и нажми «Сгенерировать».")
