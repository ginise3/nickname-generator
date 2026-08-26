"""Тексты интерфейса для локализованных версий приложения.

Каждый язык — это словарь с одинаковой структурой ключей. Логика генерации
ников (`nickname_generator.generator`) от языка не зависит — переводится
только то, что видит пользователь.
"""

from __future__ import annotations

from .generator import Style

# Порядок стилей в выпадающем списке (одинаковый для всех языков).
STYLE_ORDER = [Style.RANDOM, Style.GAMER, Style.CUTE]

TRANSLATIONS: dict[str, dict] = {
    "ru": {
        "page_title": "Генератор ников",
        "page_icon": "🎮",
        "title": "🎮 Генератор ников",
        "caption": "Придумай уникальный ник для игр, соцсетей и не только",
        "tab_generator": "🎲 Генератор ников",
        "tab_invisible": "👻 Невидимый ник",
        "sidebar": {
            "header": "Настройки",
            "base_word_label": "Слово или имя для основы ника (необязательно)",
            "base_word_placeholder": "например, Alex",
            "style_label": "Стиль",
            "style_options": {
                Style.RANDOM: "Случайный",
                Style.GAMER: "Геймерский",
                Style.CUTE: "Милый",
            },
            "count_label": "Количество ников",
            "use_numbers_label": "Добавлять числа",
            "use_leet_label": "Leet-speak (а → 4, о → 0 и т.д.)",
            "generate_button": "✨ Сгенерировать",
        },
        "results": {
            "subheader": "Результат",
            "copy_hint": "Нажми «Копировать» рядом с ником, чтобы скопировать его в буфер обмена.",
            "empty_info": "Настрой параметры слева и нажми «Сгенерировать».",
            "copy_button_label": "📋 Копировать",
            "copied_label": "✅ Скопировано",
            "failed_label": "⚠️ Не удалось",
        },
        "invisible": {
            "subheader": "Невидимый ник",
            "description": (
                "Некоторые Unicode-символы выглядят как пустота, но не являются "
                "обычным пробелом — Discord, Telegram и многие игры принимают их "
                "как имя, хотя визуально ник кажется пустым."
            ),
            "preset_label": "Платформа / вариант символа",
            "presets": {
                "discord": "Discord (Braille Pattern Blank)",
                "telegram": "Telegram (Hangul Filler)",
                "zwsp": "Zero-Width Space (для комбинаций)",
            },
            "repeat_label": "Сколько символов использовать",
            "repeat_help": "Некоторые платформы требуют минимум 2 символа для имени.",
            "updated_toast": "🔄 Ник обновлён",
            "result_ready": "✅ Готово: {count} × «{preset}» — скопируй ниже",
            "preview_label": "Твой невидимый ник (выглядит пустым, но содержит символ):",
            "copy_button_label": "📋 Копировать невидимый ник",
            "copied_label": "✅ Скопировано",
            "failed_label": "⚠️ Не удалось",
            "how_to_header": "Как использовать",
            "how_to_markdown": """
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
            """,
        },
    },
    "en": {
        "page_title": "Nickname Generator",
        "page_icon": "🎮",
        "title": "🎮 Nickname Generator",
        "caption": "Create a unique nickname for games, social media and beyond",
        "tab_generator": "🎲 Nickname Generator",
        "tab_invisible": "👻 Invisible Nickname",
        "sidebar": {
            "header": "Settings",
            "base_word_label": "Base word or name (optional)",
            "base_word_placeholder": "e.g. Alex",
            "style_label": "Style",
            "style_options": {
                Style.RANDOM: "Random",
                Style.GAMER: "Gamer",
                Style.CUTE: "Cute",
            },
            "count_label": "Number of nicknames",
            "use_numbers_label": "Add numbers",
            "use_leet_label": "Leet-speak (a → 4, o → 0, etc.)",
            "generate_button": "✨ Generate",
        },
        "results": {
            "subheader": "Results",
            "copy_hint": "Click “Copy” next to a nickname to copy it to your clipboard.",
            "empty_info": "Adjust the settings on the left and click “Generate”.",
            "copy_button_label": "📋 Copy",
            "copied_label": "✅ Copied",
            "failed_label": "⚠️ Failed",
        },
        "invisible": {
            "subheader": "Invisible Nickname",
            "description": (
                "Some Unicode characters look like empty space but aren't a "
                "regular space — Discord, Telegram and many games accept them "
                "as a name, even though the nickname appears blank."
            ),
            "preset_label": "Platform / character variant",
            "presets": {
                "discord": "Discord (Braille Pattern Blank)",
                "telegram": "Telegram (Hangul Filler)",
                "zwsp": "Zero-Width Space (for combining)",
            },
            "repeat_label": "Number of characters to use",
            "repeat_help": "Some platforms require at least 2 characters for a name.",
            "updated_toast": "🔄 Nickname updated",
            "result_ready": "✅ Ready: {count} × “{preset}” — copy it below",
            "preview_label": "Your invisible nickname (looks empty, but contains a character):",
            "copy_button_label": "📋 Copy invisible nickname",
            "copied_label": "✅ Copied",
            "failed_label": "⚠️ Failed",
            "how_to_header": "How to use it",
            "how_to_markdown": """
1. Click **"Copy invisible nickname"** above.
2. Open your profile/nickname settings in Discord, Telegram, or a game.
3. Paste the copied character into the name field (`Ctrl+V` / `⌘+V`).
4. If the platform rejects the name (says it's "empty" or "too short"),
   increase the character count with the slider above, or try another preset —
   different platforms filter out "blank" characters differently.
5. Save your changes.

**Tip:** *Braille Pattern Blank* (⠀) usually works best for Discord, while
*Hangul Filler* (ㅤ) works well for Telegram. *Zero-Width Space* is handy for
combining with other characters if you need a nickname longer than one
character.
            """,
        },
    },
}
