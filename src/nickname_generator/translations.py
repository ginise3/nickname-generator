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
    },
    "en": {
        "page_title": "Nickname Generator",
        "page_icon": "🎮",
        "title": "🎮 Nickname Generator",
        "caption": "Create a unique nickname for games, social media and beyond",
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
    },
}
