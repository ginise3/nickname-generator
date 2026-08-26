"""HTML/JS-компонент для кнопок «Копировать» внутри Streamlit."""

from __future__ import annotations

import html
import json

ROW_HEIGHT = 52
_BASE_HEIGHT = 16  # запас на отступы контейнера

_STYLE = """
<style>
  * { box-sizing: border-box; }
  body {
    margin: 0;
    font-family: "Source Sans Pro", -apple-system, BlinkMacSystemFont,
      "Segoe UI", Roboto, sans-serif;
    color: #31333f;
    background: transparent;
  }
  @media (prefers-color-scheme: dark) {
    body { color: #fafafa; }
  }
  .nick-row {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 0;
    flex-wrap: wrap;
  }
  .nick-text {
    flex: 1 1 auto;
    min-width: 120px;
    padding: 6px 10px;
    border-radius: 6px;
    background: rgba(120, 120, 120, 0.12);
    font-family: "Source Code Pro", Consolas, Monaco, monospace;
    font-size: 0.92rem;
    overflow-wrap: anywhere;
  }
  .copy-btn {
    flex: 0 0 auto;
    cursor: pointer;
    padding: 6px 14px;
    border-radius: 6px;
    border: 1px solid rgba(120, 120, 120, 0.4);
    background: rgba(120, 120, 120, 0.06);
    color: inherit;
    font-size: 0.85rem;
    transition: background 0.15s ease;
    white-space: nowrap;
  }
  .copy-btn:hover { background: rgba(120, 120, 120, 0.22); }
  .copy-btn.copied {
    border-color: rgba(46, 160, 67, 0.6);
    color: #2ea043;
  }
  @media (max-width: 420px) {
    .nick-text { flex-basis: 100%; }
    .copy-btn { flex: 1 1 auto; }
  }
</style>
"""

_SCRIPT = """
<script>
  function copyNickname(btn, text) {
    const finish = (ok) => {
      const original = btn.dataset.label;
      btn.textContent = ok ? "✅ Скопировано" : "⚠️ Не удалось";
      btn.classList.toggle("copied", ok);
      setTimeout(() => {
        btn.textContent = original;
        btn.classList.remove("copied");
      }, 1500);
    };

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard.writeText(text).then(() => finish(true)).catch(() => fallbackCopy(text, finish));
    } else {
      fallbackCopy(text, finish);
    }
  }

  function fallbackCopy(text, finish) {
    try {
      const area = document.createElement("textarea");
      area.value = text;
      area.style.position = "fixed";
      area.style.opacity = "0";
      document.body.appendChild(area);
      area.focus();
      area.select();
      const ok = document.execCommand("copy");
      document.body.removeChild(area);
      finish(ok);
    } catch (err) {
      finish(false);
    }
  }
</script>
"""


def _row_html(text: str, label: str = "📋 Копировать") -> str:
    escaped_display = html.escape(text)
    js_text = json.dumps(text)
    return f"""
    <div class="nick-row">
      <code class="nick-text">{escaped_display}</code>
      <button class="copy-btn" data-label="{html.escape(label)}"
              onclick="copyNickname(this, {js_text})">{html.escape(label)}</button>
    </div>
    """


def build_copy_list_html(items: list[str]) -> tuple[str, int]:
    """Строит один HTML-блок со списком ников и кнопками копирования.

    Возвращает (html, height) — height подходит для components.html().
    """
    rows = "\n".join(_row_html(item) for item in items)
    document = f"{_STYLE}<div>{rows}</div>{_SCRIPT}"
    height = _BASE_HEIGHT + ROW_HEIGHT * max(len(items), 1)
    return document, height


def build_single_copy_html(text: str, label: str = "📋 Копировать") -> tuple[str, int]:
    """Строит компактный HTML-блок с одним ником и кнопкой копирования."""
    document = f"{_STYLE}<div>{_row_html(text, label)}</div>{_SCRIPT}"
    return document, _BASE_HEIGHT + ROW_HEIGHT
