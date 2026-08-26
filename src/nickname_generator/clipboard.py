"""Одностороннее HTML/JS-отображение списка ников с кнопками «Копировать».

Используется для списка сгенерированных ников (список из N ников).
Копирование выполняется полностью на стороне JS внутри iframe — сюда не
передаётся результат клика обратно в Python, поэтому подтверждение об
успехе тоже рисуется прямо в этом же HTML (см. `.copy-banner`).

Важный нюанс: Streamlit рендерит `components.html(...)` внутри
сэндбоксированного iframe, у которого браузер по умолчанию блокирует
Clipboard API через Permissions Policy (даже если сам JS в iframe исполняется
нормально) — из-за этого `navigator.clipboard.writeText()`, вызванный из
локального `window`, тихо падает с ошибкой, и кнопка «не копирует». Iframe
Streamlit при этом помечен `allow-same-origin`, поэтому у него есть доступ к
`window.parent` (родительскому окну приложения) — вызывая Clipboard API
именно через него, мы выполняем копирование в контексте верхнеуровневого
документа, для которого политика разрешений это разрешает. См. `copyText()`
и `showToast()` ниже.
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
  // Родительское окно (сам Streamlit-апп), если оно доступно — iframe этого
  // компонента помечен Streamlit'ом allow-same-origin, так что доступ есть.
  function parentWindow() {{
    try {{
      if (window.parent && window.parent !== window && window.parent.document) {{
        return window.parent;
      }}
    }} catch (err) {{
      // Кросс-origin — недоступно, работаем только с локальным окном.
    }}
    return null;
  }}

  // Пытается записать текст в буфер обмена: сперва через Clipboard API
  // родительского (верхнеуровневого) окна — там нет ограничений Permissions
  // Policy, которые блокируют этот же вызов внутри самого iframe; затем —
  // через локальный Clipboard API; и в последнюю очередь — старым
  // document.execCommand("copy") (тоже сначала в родительском документе,
  // затем в локальном), на случай браузеров без поддержки Clipboard API.
  function copyText(text) {{
    const pw = parentWindow();
    const clipboardAttempts = [];
    if (pw && pw.navigator && pw.navigator.clipboard && pw.isSecureContext) {{
      clipboardAttempts.push(() => pw.navigator.clipboard.writeText(text));
    }}
    if (navigator.clipboard && window.isSecureContext) {{
      clipboardAttempts.push(() => navigator.clipboard.writeText(text));
    }}

    const tryClipboard = (i) => {{
      if (i >= clipboardAttempts.length) {{
        return Promise.reject(new Error("Clipboard API unavailable"));
      }}
      return clipboardAttempts[i]().catch(() => tryClipboard(i + 1));
    }};

    return tryClipboard(0).catch(() => {{
      const docs = [];
      if (pw && pw.document) docs.push(pw.document);
      docs.push(document);
      for (const doc of docs) {{
        try {{
          const area = doc.createElement("textarea");
          area.value = text;
          area.style.position = "fixed";
          area.style.opacity = "0";
          doc.body.appendChild(area);
          area.focus();
          area.select();
          const ok = doc.execCommand("copy");
          doc.body.removeChild(area);
          if (ok) return Promise.resolve();
        }} catch (err) {{
          // пробуем следующий документ
        }}
      }}
      return Promise.reject(new Error("execCommand copy failed"));
    }});
  }}

  // Настоящий всплывающий тост поверх ВСЕГО приложения (не только этой
  // строки) — рисуется в родительском документе, если он доступен, чтобы
  // не быть обрезанным маленькой высотой iframe-компонента.
  function showToast(ok) {{
    const pw = parentWindow();
    if (!pw) return false;
    try {{
      const doc = pw.document;
      let toast = doc.getElementById("nickname-copy-toast");
      if (!toast) {{
        toast = doc.createElement("div");
        toast.id = "nickname-copy-toast";
        toast.setAttribute("role", "status");
        toast.setAttribute("aria-live", "polite");
        toast.style.position = "fixed";
        toast.style.left = "50%";
        toast.style.bottom = "32px";
        toast.style.transform = "translateX(-50%) translateY(12px)";
        toast.style.zIndex = "999999";
        toast.style.padding = "10px 18px";
        toast.style.borderRadius = "8px";
        toast.style.fontFamily =
          '"Source Sans Pro", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
        toast.style.fontSize = "0.9rem";
        toast.style.fontWeight = "600";
        toast.style.color = "#ffffff";
        toast.style.boxShadow = "0 4px 14px rgba(0, 0, 0, 0.25)";
        toast.style.opacity = "0";
        toast.style.pointerEvents = "none";
        toast.style.transition = "opacity 0.18s ease, transform 0.18s ease";
        doc.body.appendChild(toast);
      }}
      toast.textContent = ok ? {json.dumps(copied_label)} : {json.dumps(failed_label)};
      toast.style.background = ok ? "#21a545" : "#d93025";
      toast.style.opacity = "1";
      toast.style.transform = "translateX(-50%) translateY(0)";
      clearTimeout(toast._hideTimer);
      toast._hideTimer = setTimeout(() => {{
        toast.style.opacity = "0";
        toast.style.transform = "translateX(-50%) translateY(12px)";
      }}, 1800);
      return true;
    }} catch (err) {{
      return false;
    }}
  }}

  function copyNickname(btn, text) {{
    const row = btn.closest(".nick-row");
    const banner = row ? row.querySelector(".copy-banner") : null;

    const finish = (ok) => {{
      const shownAsToast = showToast(ok);
      if (shownAsToast) return;
      // Родительское окно недоступно (например, HTML открыт напрямую,
      // не внутри Streamlit) — показываем баннер прямо в строке.
      if (!banner) return;
      banner.textContent = ok ? {json.dumps(copied_label)} : {json.dumps(failed_label)};
      banner.classList.toggle("error", !ok);
      banner.classList.add("show");
      clearTimeout(banner._hideTimer);
      banner._hideTimer = setTimeout(() => {{
        banner.classList.remove("show", "error");
      }}, 1800);
    }};

    copyText(text).then(() => finish(true)).catch(() => finish(false));
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
