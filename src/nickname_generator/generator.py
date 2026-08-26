"""Логика генерации ников."""

from __future__ import annotations

import random
from enum import Enum

from .data import (
    ADJECTIVES,
    CUTE_ADJECTIVES,
    CUTE_NOUNS,
    LEET_MAP,
    NOUNS,
    SEPARATORS,
)


class Style(str, Enum):
    """Стиль генерируемых ников."""

    GAMER = "gamer"
    CUTE = "cute"
    RANDOM = "random"


def _apply_leet(word: str) -> str:
    """Заменяет часть букв на цифры в стиле leet-speak."""
    return "".join(LEET_MAP.get(ch.lower(), ch) for ch in word)


def _random_number(min_value: int = 1, max_value: int = 999) -> str:
    return str(random.randint(min_value, max_value))


def _build_nickname(
    base_word: str | None,
    style: Style,
    use_numbers: bool,
    use_leet: bool,
) -> str:
    if style == Style.CUTE:
        adjectives, nouns = CUTE_ADJECTIVES, CUTE_NOUNS
    else:
        adjectives, nouns = ADJECTIVES, NOUNS

    adjective = random.choice(adjectives)
    noun = base_word.capitalize() if base_word else random.choice(nouns)
    separator = random.choice(SEPARATORS)

    parts = [adjective, noun]
    nickname = separator.join(parts)

    if use_leet:
        nickname = _apply_leet(nickname)

    if use_numbers:
        nickname = f"{nickname}{separator}{_random_number()}"

    return nickname


def generate_nicknames(
    base_word: str | None = None,
    style: Style | str = Style.RANDOM,
    count: int = 10,
    use_numbers: bool = False,
    use_leet: bool = False,
) -> list[str]:
    """Генерирует список уникальных ников.

    Args:
        base_word: слово, которое нужно включить в ник (например, имя).
        style: стиль генерации — "gamer", "cute" или "random".
        count: сколько ников сгенерировать.
        use_numbers: добавлять ли случайные числа в конец.
        use_leet: заменять ли буквы на похожие цифры (leet-speak).

    Returns:
        Список сгенерированных ников без повторов.
    """
    if count <= 0:
        return []

    style_enum = Style(style) if not isinstance(style, Style) else style
    if style_enum == Style.RANDOM:
        pool: list[Style] = [Style.GAMER, Style.CUTE]
    else:
        pool = [style_enum]

    nicknames: set[str] = set()
    attempts = 0
    max_attempts = count * 20

    while len(nicknames) < count and attempts < max_attempts:
        chosen_style = random.choice(pool)
        nicknames.add(
            _build_nickname(
                base_word=base_word,
                style=chosen_style,
                use_numbers=use_numbers,
                use_leet=use_leet,
            )
        )
        attempts += 1

    return list(nicknames)
