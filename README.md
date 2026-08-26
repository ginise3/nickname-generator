# Nickname Generator

Веб-приложение на [Streamlit](https://streamlit.io/) для генерации уникальных ников — для игр, соцсетей и не только.

## Возможности

- Стили: геймерский, милый, случайный
- Основа из своего слова/имени
- Добавление случайных чисел
- Leet-speak преобразование (`a` → `4`, `o` → `0` и т.д.)

## Структура проекта

```
nickname-generator/
├── app.py                          # точка входа Streamlit-приложения
├── src/
│   └── nickname_generator/
│       ├── __init__.py
│       ├── generator.py            # логика генерации ников
│       └── data.py                 # словари прилагательных/существительных
├── tests/
│   └── test_generator.py
├── requirements.txt
└── README.md
```

## Установка и запуск

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py
```

Приложение откроется в браузере по адресу `http://localhost:8501`.

## Тесты

```bash
pip install pytest
pytest
```
