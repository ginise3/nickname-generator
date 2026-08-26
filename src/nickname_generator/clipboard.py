"""Одностороннее HTML/JS-отображение списка ников с кнопками «Копировать».

Используется для списка сгенерированных ников (список из N ников).
Копирование выполняется полностью на стороне JS внутри iframe — сюда не
передаётся результат клика обратно в Python, поэтому подтверждение об
успехе тоже рисуется прямо в этом же HTML (см. `.copy-banner`).
"""

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
    position: relative;
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
  /* Заметное подтверждение результата копирования — перекрывает всю строку,
     поэтому не требует пересчёта высоты iframe-компонента. */
  .copy-banner {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    border-radius: 6px;
    font-weight: 600;
    font-size: 0.9rem;
    color: #ffffff;
    background: #21a545;
    opacity: 0;
    transform: translateY(-2px);
    pointer-events: none;
    transition: opacity 0.18s ease, transform 0.18s ease;
  }
  .copy-banner.show { opacity: 1; transform: translateY(0); }
  .copy-banner.error { background: #d93025; }
  @media (max-width: 420px) {
    .nick-text { flex-basis: 100%; }
    .copy-btn { flex: 1 1 auto; }
  }
</style>
"""


def _script(copied_label: str, failed_label: str) -> str:
    return f"""
<script>
  function copyNickname(btn, text) {{
    const row = btn.closest(".nick-row");
    const banner = row ? row.querySelector(".copy-banner") : null;

    const finish = (ok) => {{
      if (!banner) return;
      banner.textContent = ok ? {json.dumps(copied_label)} : {json.dumps(failed_label)};
      banner.classList.toggle("error", !ok);
      banner.classList.add("show");
      clearTimeout(banner._hideTimer);
      banner._hideTimer = setTimeout(() => {{
        banner.classList.remove("show", "error");
      }}, 1800);
    }};

    if (navigator.clipboard && window.isSecureContext) {{
      navigator.clipboard.writeText(text).then(() => finish(true)).catch(() => fallbackCopy(text, finish));
    }} else {{
      fallbackCopy(text, finish);
    }}
  }}

  function fallbackCopy(text, finish) {{
    try {{
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
    }} catch (err) {{
      finish(false);
    }}
  }}
</script>
"""


def _row_html(text: str, label: str) -> str:
    escaped_display = html.escape(text)
    js_text = json.dumps(text)
    return f"""
    <div class="nick-row">
      <code class="nick-text">{escaped_display}</code>
      <button class="copy-btn" data-label="{html.escape(label)}"
              onclick="copyNickname(this, {js_text})">{html.escape(label)}</button>
      <div class="copy-banner" role="status" aria-live="polite"></div>
    </div>
    """


def build_copy_list_html(
    items: list[str],
    label: str = "📋 Копировать",
    copied_label: str = "✅ Скопировано",
    failed_label: str = "⚠️ Не удалось",
) -> tuple[str, int]:
    """Строит один HTML-блок со списком ников и кнопками копирования.

    Возвращает (html, height) — height подходит для components.html().
    """
    rows = "\n".join(_row_html(item, label) for item in items)
    document = f"{_STYLE}<div>{rows}</div>{_script(copied_label, failed_label)}"
    height = _BASE_HEIGHT + ROW_HEIGHT * max(len(items), 1)
    return document, height
