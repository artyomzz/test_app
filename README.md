# Тестовое задание

Ссылка на постановку: https://docs.google.com/document/d/1Xw4L-_riLixQFA127Uyvoq3JNrJm6hgSr7c7ux6z_fY

## Стек технологий:

- python3.10
- pip
- fastapi - web client для rest api
- postgres 15


## Настройка докера

Пример использования докера:

1. `docker-compose up`
2. Приложение будет доступно на порту `8000`


## Документация

- REST документация хранится по пути `/docs` или `/redoc`

## Переменные окружения

| Наименование | Описание | Пример |
|--------------|----------|--------|
|DB_HOST|Host|postgres|
|DB_PORT|Порт|5432|
|DB_USER|Пользователь|postgres|
|DB_PASSWORD|Пароль|postgres|
|DB_NAME|Имя базы данных|postgres|
|POSTGRES_DB|Имя базы данных для запуска в docker|postgres|
|POSTGRES_USER|Пользователь для запуска в docker|postgres|
|POSTGRES_PASSWORD|Пароль для запуска в docker|postgres|


## Разработка

1. Устновить зависимости `pip install -r requirements.txt`
2. Создать .env файл и добавить переменные окружения
3. запуск производится с помощью команды `uvicorn src.main:app`


## Alembic

Миграции пишутся с помощью alembic:

1. Автоматическая генерация миграции: `alembic revision --autogenerate -m "Added * table"`
2. Накатка миграций: `alembic upgrade head`
