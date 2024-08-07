# Description

[![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/likeinlife/memes?label=version)](https://github.com/likeinlife/memes/releases)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<a href="http://mypy-lang.org/" target="_blank"><img src="https://img.shields.io/badge/mypy-checked-1F5082.svg" alt="Mypy checked"></a>

АПИ для загрузки/получения/редактирования мемов.

Мем состоит из текста и картинки.

Картинки сохраняются в S3 хранилище.

# Диаграмма

![](./diagrams/out/c4.png)

# Запуск

1. `make dev-storages` - запустить PostgreSQL, MinIO
2. `make dev-app` - запустить приложения
3. `make down-all` - закрыть приложения
4. `make down-storages-v` - удалить volume хранилищ

# Swagger

Swagger доступен по адресу `http://localhost:8000/api/docs`

# Тестирование

1. `cd memes/public` - перейти в тестируемую директорию
2. `poetry install --with test` - установить зависимости для тестирования
3. `pytest` - запустить тесты

![](./static/tests.png)

# Описание работы

Проект представляет собой два сервиса: PublicAPI и Gateway.

- PublicAPI - публичное апи для действий с мемами.
- Gateway - закрытое апи для взаимодействия с S3 хранилищем.

Приложения построены с оглядкой на чистую архитектуру.

В каждом выделены слои:

- `domain` - домен
- `logic` - бизнес-логика: use-cases, interactors (в Gateway отсутствует, т.к. нет необходимости)
- `infra` - репозитории, сервисы
- `presentation` - представление

В качестве DI-библиотеки применяется Dishka. Конфигурация описана в каждом проекте в пакете `container`

# Время работы

Полное время работы над проектом составило 8 часов.

![](./static/worktime_metrics.png)

# Стек

- Python3.11
- FastAPI
- MinIO
- PostgreSQL
- Docker
- SQLALchemy
- alembic
- dishka
- pytest

# Скриншоты

Скриншоты Swagger можно посмотреть в папке `./static/`
