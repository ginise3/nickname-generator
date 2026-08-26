# Nickname Generator

Веб-приложение на [Streamlit](https://streamlit.io/) для генерации уникальных ников — для игр, соцсетей и не только.

Доступно в двух локализованных версиях с общей логикой генерации:

- 🇷🇺 `app_ru.py` — интерфейс на русском
- 🇬🇧 `app_en.py` — interface in English

## Возможности

- Стили: геймерский, милый, случайный
- Основа из своего слова/имени
- Добавление случайных чисел
- Leet-speak преобразование (`a` → `4`, `o` → `0` и т.д.)
- Кнопки копирования в буфер обмена для каждого ника

## Структура проекта

```
nickname-generator/
├── app.py                          # алиас на русскую версию (для локального запуска)
├── app_ru.py                       # точка входа: русская версия (Streamlit Cloud)
├── app_en.py                       # точка входа: английская версия (Streamlit Cloud)
├── src/
│   └── nickname_generator/
│       ├── __init__.py
│       ├── generator.py            # логика генерации ников (не зависит от языка)
│       ├── data.py                 # словари прилагательных/существительных
│       ├── translations.py         # тексты интерфейса на ru/en
│       ├── clipboard.py            # HTML/JS-компонент кнопок «Копировать»
│       └── webapp.py               # общий UI, параметризуемый языком
├── tests/
│   └── test_generator.py
├── requirements.txt
└── README.md
```

Вся логика генерации и данные лежат в `src/nickname_generator/` и не дублируются между языковыми версиями — `app_ru.py` и `app_en.py` лишь вызывают `webapp.run_app("ru" | "en")` с разным набором текстов из `translations.py`.

## Установка и запуск

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app_ru.py        # русская версия
streamlit run app_en.py        # English version
```

Приложение откроется в браузере по адресу `http://localhost:8501`.

## Деплой на Streamlit Cloud

Каждую локализацию можно задеплоить как отдельный проект на [Streamlit Cloud](https://streamlit.io/cloud), указав в настройках проекта разные main-файлы для одного и того же репозитория:

- Проект 1: main file → `app_ru.py`
- Проект 2: main file → `app_en.py`

## Тесты

```bash
pip install pytest
pytest
```
