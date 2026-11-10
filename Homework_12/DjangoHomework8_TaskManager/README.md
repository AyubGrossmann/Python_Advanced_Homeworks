# Домашнее задание 12 — Django REST Framework API

Проект продолжает Task Manager из ДЗ №8–11. Модели Task, SubTask и Category,
поля и предыдущие настройки сохранены. Для ДЗ №12 добавлен REST API для модели Task.

## 1. Установка

Откройте папку `DjangoHomework8_TaskManager` в PyCharm.

Создайте и активируйте виртуальное окружение (если ещё не создано):

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Установите зависимости:

```bash
pip install -r requirements.txt
```

## 2. Миграции и запуск

```bash
python manage.py migrate
python manage.py runserver
```

## 3. API endpoints

Базовый адрес: `http://127.0.0.1:8000/api/`

| Метод | URL | Назначение |
|---|---|---|
| POST | `/api/tasks/` | Создать задачу |
| GET | `/api/tasks/` | Получить список задач |
| GET | `/api/tasks/1/` | Получить задачу с ID 1 |
| GET | `/api/tasks/statistics/` | Получить статистику |

## 4. Примеры тестирования

Можно использовать браузер, Postman или встроенный DRF Browsable API.

### Создание задачи

POST `http://127.0.0.1:8000/api/tasks/`

Выберите Body → raw → JSON:

```json
{
    "title": "Prepare API project",
    "description": "Create API endpoints for Task Manager.",
    "status": "New",
    "deadline": "2026-12-15T18:00:00Z"
}
```

В ответе должен появиться созданный объект с `id` и `created_at`.

Допустимые значения `status`:
- `New`
- `In progress`
- `Pending`
- `Blocked`
- `Done`

### Получение списка задач

GET `http://127.0.0.1:8000/api/tasks/`

### Получение одной задачи

GET `http://127.0.0.1:8000/api/tasks/1/`

Замените `1` на ID существующей задачи.

### Получение статистики

GET `http://127.0.0.1:8000/api/tasks/statistics/`

Пример ответа:

```json
{
    "total_tasks": 5,
    "tasks_by_status": {
        "New": 2,
        "In progress": 1,
        "Done": 2
    },
    "overdue_tasks": 1
}
```

Числа в примере условные: реальные значения зависят от записей в вашей базе.
Просроченными считаются задачи с прошедшим дедлайном и статусом не `Done`.

## 5. Структура добавленных файлов

- `tasks/serializers.py` — сериализатор Task.
- `tasks/views.py` — представления для создания, списка, одной задачи и статистики.
- `tasks/urls.py` — маршруты API.
- `djangohomework8/urls.py` — подключение маршрутов приложения.
- `requirements.txt` — добавлена зависимость Django REST Framework.


Для ДЗ №12 новые миграции не нужны: структура моделей не менялась.
