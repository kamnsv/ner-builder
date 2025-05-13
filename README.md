# Построение графа знаний

![](https://img.shields.io/badge/python-3.11-blue)


Проект предназначен для построения графа знаний из текста при помощи локальной LLM.

Основное решение в виде документированного API (swagger). 

## Запуск

При необходимости переопределения переменных окружений скопируйте `example.env` в `.env`.

Для запуска контейнеров введите:

```
docker-compose up -d
```

Будет поднято 2 контейнера: 

1. `ner_app` логика приложения на Python (FastAPI).
2. `ner_kg` графовая база данных Neo4j.

После первого запуска загрузятся все необходимые модели.

## Тесты 

- Для проведения тестов нужен `python => 3.10` с библиотекой `requests`.
- Для запуска тестов, добавьте переменную `test_api` с адресом тестируемого API, по умолчанию `http://localhost:8000/api`.

> Проверти версию `python` и наличие библиотеки `requests`:

```
python -V
> 3.10

python -m pip freeze | grep requests
> requests=>2.*
```

В случае отсутствия установите библиотеку `requests`:

```
python -m pip install requests
```

**Запуск тестов**

```
# в PowerShell
$env:TEST_API="http://localhost:8000/api"; python -m unittest discover -s tests -v 

# в Linux/macOS
TEST_API=http://localhost:8000/api python -m unittest discover -s tests -v    
или
export TEST_API=http://localhost:8000/api && python3 -m unittest discover -s tests -v

# в cmd     
set TEST_API=http://localhost:8000/api
python -m unittest discover -s tests -v  
```

> Замените `python` на подходящую версию (python3 или python3.10)

## Основные компоненты

![](docs/umls/uml.png)

1. [Граф знаний](docs/kg.md)
2. [Языковая модель и особенности тестирования](docs/llm.md)
