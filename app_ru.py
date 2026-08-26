"""Точка входа: русскоязычная версия приложения (для Streamlit Cloud)."""

from __future__ import annotations

import sys
from pathlib import Path

# Позволяет запускать `streamlit run app_ru.py` без предварительной установки пакета.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nickname_generator.webapp import run_app

run_app("ru")
