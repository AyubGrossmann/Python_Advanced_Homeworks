# Домашнее задание 18 — JWT, permissions и глобальная пагинация

Проект продолжает Task Manager из ДЗ №8–17. Добавлена JWT-аутентификация
с помощью SimpleJWT, права доступа для API и глобальная пагинация на 5 объектов.

## Что сделано

### 1. JWT-аутентификация

Установлена библиотека `djangorestframework-simplejwt`.

В `settings.py` добавлены:
- `JWTAuthentication`;
- `SessionAuthentication`;
- глобальные настройки REST Framework.

Маршруты:
- POST `/api/token/` — получить access и refresh токены;
- POST `/api/token/refresh/` — обновить access токен.

Для получения токена нужен существующий пользователь Django. Создать его можно:

```bash
python manage.py createsuperuser
```

### 2. Права доступа

Используется `IsAuthenticatedOrReadOnly`.

Это означает:
- GET-запросы (чтение) доступны всем;
- POST, PUT, PATCH и DELETE доступны только авторизованным пользователям.

Это правило установлено для задач, подзадач, категорий и статистики.

### 3. Глобальная пагинация

Сохранён `CursorPagination` из ДЗ №17. Размер страницы изменён на 5 объектов.
CursorPagination не использует обычные номера страниц и offset.

В ответе списка будут `next`, `previous` и `results`.
Для следующей страницы используйте ссылку `next`, которую вернул сервер.

## Установка и запуск

Откройте папку `DjangoHomework8_TaskManager` в PyCharm.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Миграции моделей для ДЗ №18 не менялись.

## Проверка JWT через Postman

### Шаг 1. Получить токен

POST:

`http://127.0.0.1:8000/api/token/`

Body → raw → JSON:

```json
{
    "username": "ваш_логин",
    "password": "ваш_пароль"
}
```

В ответе будут `access` и `refresh`.

### Шаг 2. Проверить защищённое действие без токена

Попробуйте POST:

`http://127.0.0.1:8000/api/tasks/`

Без заголовка Authorization сервер должен вернуть `401 Unauthorized`
(или `403 Forbidden` при некоторых настройках аутентификации).

### Шаг 3. Создать задачу с токеном

В Headers добавьте:

```text
Authorization: Bearer ВАШ_ACCESS_TOKEN
```

Теперь POST `/api/tasks/` должен быть доступен.

### Шаг 4. Обновить токен

POST:

`http://127.0.0.1:8000/api/token/refresh/`

Body:

```json
{
    "refresh": "ВАШ_REFRESH_TOKEN"
}
```

В ответе придёт новый access token.

## Проверка пагинации

Откройте:

`http://127.0.0.1:8000/api/tasks/`

В поле `results` должно быть не больше 5 объектов.
Если объектов больше, в ответе будет ссылка `next`.

Глобальная настройка применяется к спискам задач, подзадач и категорий.

## Примечание

Access token — короткоживущий токен для запросов к API.
Refresh token используется для получения нового access token.
Не публикуйте реальные токены и пароль в GitHub или скриншотах.
