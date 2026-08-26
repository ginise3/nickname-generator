"""Точка входа по умолчанию (алиас на русскую версию).

Для деплоя на Streamlit Cloud как двух отдельных проектов используйте
`app_ru.py` и `app_en.py` напрямую.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from nickname_generator.webapp import run_app

run_app("ru")
