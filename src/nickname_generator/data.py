"""Наборы слов и символов, используемые генератором ников."""

ADJECTIVES = [
    "Shadow", "Silent", "Crimson", "Frozen", "Mystic", "Rapid", "Golden",
    "Dark", "Silver", "Iron", "Savage", "Lunar", "Solar", "Phantom",
    "Rogue", "Feral", "Vivid", "Cosmic", "Toxic", "Blazing", "Frosty",
    "Wild", "Electric", "Ancient", "Neon", "Grim", "Radiant", "Sneaky",
]

NOUNS = [
    "Wolf", "Dragon", "Phoenix", "Ninja", "Falcon", "Tiger", "Reaper",
    "Knight", "Ghost", "Viper", "Panther", "Hunter", "Raven", "Storm",
    "Blade", "Wizard", "Titan", "Fox", "Bear", "Hawk", "Samurai",
    "Warrior", "Sniper", "Nomad", "Specter", "Rider", "Cobra", "Legend",
]

CUTE_ADJECTIVES = [
    "Sweet", "Fluffy", "Tiny", "Sunny", "Cozy", "Bubbly", "Sparkly",
    "Cuddly", "Giggly", "Dreamy", "Sugar", "Peachy", "Honey", "Snuggly",
]

CUTE_NOUNS = [
    "Bunny", "Panda", "Kitty", "Puppy", "Cupcake", "Bean", "Peach",
    "Cookie", "Muffin", "Marshmallow", "Petal", "Star", "Cloud", "Berry",
]

LEET_MAP = {
    "a": "4", "e": "3", "i": "1", "o": "0", "s": "5", "t": "7",
}

SEPARATORS = ["", "_", "-", "."]

# Unicode-символы, которые отображаются как пустота, но не являются обычным
# пробелом — платформы вроде Discord/Telegram отклоняют ники из "настоящих"
# пробелов, но принимают эти символы.
# Ключи нейтральны (не привязаны к языку интерфейса) — подписи для UI берутся
# из nickname_generator.translations.
INVISIBLE_CHARS = {
    "discord": "⠀",  # Braille Pattern Blank
    "telegram": "ㅤ",  # Hangul Filler
    "zwsp": "​",  # Zero-Width Space — удобен для комбинаций
}

# Порядок отображения пресетов в UI.
INVISIBLE_CHAR_ORDER = ["discord", "telegram", "zwsp"]

