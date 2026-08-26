"""Entry point: English version of the app (for Streamlit Cloud)."""

from __future__ import annotations

import sys
from pathlib import Path

# Lets you run `streamlit run app_en.py` without installing the package first.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from nickname_generator.webapp import run_app

run_app("en")
