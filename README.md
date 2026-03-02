# Habit Tracker API

Backend-сервис для трекинга полезных привычек на Django REST Framework.
Проект реализован как API для SPA-клиента с JWT-аутентификацией, правами доступа, бизнес-валидацией и Telegram-напоминаниями через Celery.

## О проекте

Сервис помогает пользователю:

- создавать полезные и приятные привычки;
- связывать полезную привычку с приятной (как награда);
- задавать периодичность и длительность выполнения;
- публиковать привычки в общий список;
- получать напоминания в Telegram.

## Основные возможности

- JWT-аутентификация (`register`, `token`, `token/refresh`);
- CRUD только для привычек владельца;
- публичный read-only список привычек;
- пагинация по 5 элементов;
- валидаторы;
- CORS для подключения фронтенда;
- Swagger-документация API;
- отложенные Telegram-напоминания через Celery + Redis.

---

## Технологии

- Python 3.13+
- Django 6
- Django REST Framework
- SimpleJWT
- Celery
- Redis
- drf-yasg (Swagger)

---

## Быстрый старт

### 1) Установка зависимостей

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2) Настройка окружения

Создайте `.env` на основе `env.example`.

### 3) Миграции

```bash
python manage.py migrate
```

### 4) Запуск API

```bash
python manage.py runserver
```

API будет доступен по адресу:
```
http://localhost:8000
```
### 5) Запуск Redis (локально)

Установка на Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y redis-server
```

Запуск:

```bash
sudo systemctl enable --now redis-server
```

Проверка:

```bash
redis-cli ping
```

### 6) Запуск Celery

В двух отдельных окнах терминала:

```bash
celery -A config worker -l info
```
```
celery -A config beat -l info
```

---

## Документация API

- `http://127.0.0.1:8000/swagger/`

---

## Аутентификация

Для защищенных endpoint используйте заголовок:

`Authorization: Bearer <access_token>`

---

## API: (Postman)
### Узнайте свой id Telegram:
Открой в Telegram бота @userinfobot (или @getmyid_bot).
Нажми Start.
Скопируйте поле 
Id / Chat ID и укажи его при регистрации.

### 1) Регистрация

POST
```
http://localhost/api/users/register/`
```
```json
{
  "username": "user_name",
  "password": "StrongPass123",
  "telegram_chat_id": "12345678"
}
```

Примечания:

- `email` необязателен;
- `telegram_chat_id` можно передать сразу или установить позже отдельным запросом.
- Регистрация без `telegram_chat_id` допустима: аккаунт создается, но Telegram-напоминания начнут работать только после сохранения `chat_id`.

### 2) Получение JWT

POST 
```
http://localhost/api/users/token/
```
```json
{
  "username": "user_name",
  "password": "StrongPass123"
}
```

Ответ содержит `access` и `refresh`.

### 3) Обновление telegram_chat_id после регистрации

PATCH 
```
http://localhost/api/users/telegram-chat-id/
```
```json
{
  "telegram_chat_id": "12345678"
}
```

Требуется JWT.

### 4) Создание привычки

POST 

```
http://localhost/api/habits/

```
Пример приятной привычки:

```json
{
  "place": "Дом",
  "time": "21:35:00",
  "action": "Принять ванну",
  "is_pleasant": true,
  "periodicity": 1,
  "execution_time": 90,
  "is_public": false
}
```

Пример полезной привычки с наградой:

```json
{
  "place": "Дом",
  "time": "21:30:00",
  "action": "Читать 10 страниц",
  "is_pleasant": false,
  "periodicity": 1,
  "reward": "Чашка чая",
  "execution_time": 120,
  "is_public": false
}
```

### 5) Список своих привычек

GET

```
http://localhost/api/habits/
```
Пагинация: 5 элементов на страницу.

### 6) Получение/изменение/удаление привычки

- GET ```http://localhost/api/habits/<id>/```
- PATCH ```http://localhost/api/habits/<id>/```
- DELETE ```http://localhost/api/habits/<id>/```

### 7) Список публичных привычек

GET 
```
http://localhost/api/habits/public/
```
---

## Бизнес-правила (валидаторы)

1. Нельзя одновременно указывать `related_habit` и `reward`.
2. `execution_time` не может превышать 120 секунд.
3. В `related_habit` можно указывать только приятную привычку (`is_pleasant=true`).
4. У приятной привычки не может быть `reward` или `related_habit`.
5. Полезная привычка обязана иметь `reward` или `related_habit`.
6. `periodicity` должна быть в диапазоне от 1 до 7 дней.



Проверка:

1. Убедитесь, что запущены `worker` и `beat`.
2. Создайте привычку с актуальным временем и нужной периодичностью.
3. Дождитесь времени выполнения — уведомление придет в Telegram.



## Проверки

### Тесты

```bash
python manage.py test
```

### Покрытие

```bash
coverage run manage.py test
coverage report -m
```


Миграции исключены в [.flake8](.flake8).

### Swagger-документация

Откройте в браузере:
```url
http://localhost:8000/swagger/
```


### Проверка публичного списка без авторизации

```bash
http://localhost:8000/api/habits/public/
```

### Проверка пагинации
GET Authorization: Bearer <access_token>

```bash
http://localhost:8000/api/habits/?page=1
```

### Проверка Telegram

Проверка доступности бота и тестовое сообщение:

```bash
python manage.py telegram_check --chat-id <chat_id> --text "Привет, Я 🤖 Habbit_Bot из твоего тестового запроса."
```

Если передать только `--chat-id`, сообщение будет отправлено со стандартным текстом.
