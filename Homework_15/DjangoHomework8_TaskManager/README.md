# Домашнее задание 15 — Generic Views, CRUD, фильтрация, поиск и сортировка

Проект продолжает Task Manager из ДЗ №8–14. Модели, сериализаторы и предыдущие
функции сохранены. Функциональность списка и деталей задач/подзадач переведена
на Generic Views.

## Что реализовано

### Задание 1. Generic Views для Task

- `TaskListCreateAPIView` — наследуется от `ListCreateAPIView`.
  - GET: получить список задач.
  - POST: создать задачу.
- `TaskRetrieveUpdateDestroyAPIView` — наследуется от
  `RetrieveUpdateDestroyAPIView`.
  - GET: получить задачу по ID.
  - PUT/PATCH: обновить задачу.
  - DELETE: удалить задачу.

Фильтры:
- `status` — фильтр по статусу;
- `deadline` — фильтр по дедлайну.

Поиск:
- `search` — поиск по `title` и `description`.

Сортировка:
- `ordering=created_at` — от старых к новым;
- `ordering=-created_at` — от новых к старым (по умолчанию).

### Задание 2. Generic Views для SubTask

- `SubTaskListCreateView` — список и создание подзадач.
- `SubTaskRetrieveUpdateDestroyView` — получение, обновление и удаление подзадачи.

Для подзадач также настроены фильтры `status`, `deadline`, поиск по `title`,
`description` и сортировка по `created_at`.

### Статистика

Endpoint `/api/tasks/statistics/` из предыдущих заданий сохранён.

## Установка и запуск

Откройте папку `DjangoHomework8_TaskManager` в PyCharm.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## API endpoints

| Метод | URL | Назначение |
|---|---|---|
| GET | `/api/tasks/` | Список задач |
| POST | `/api/tasks/` | Создание задачи |
| GET | `/api/tasks/1/` | Получение задачи |
| PUT/PATCH | `/api/tasks/1/` | Обновление задачи |
| DELETE | `/api/tasks/1/` | Удаление задачи |
| GET | `/api/tasks/statistics/` | Статистика |
| GET | `/api/subtasks/` | Список подзадач |
| POST | `/api/subtasks/` | Создание подзадачи |
| GET | `/api/subtasks/1/` | Получение подзадачи |
| PUT/PATCH | `/api/subtasks/1/` | Обновление подзадачи |
| DELETE | `/api/subtasks/1/` | Удаление подзадачи |

Замените `1` на ID существующей записи.

## Примеры фильтрации, поиска и сортировки

### Фильтр по статусу

```text
/api/tasks/?status=New
/api/subtasks/?status=Done
```

### Фильтр по дедлайну

```text
/api/tasks/?deadline=2026-12-20T18:00:00Z
/api/subtasks/?deadline=2026-12-20T18:00:00Z
```

### Поиск по названию или описанию

```text
/api/tasks/?search=presentation
/api/subtasks/?search=documentation
```

### Сортировка

```text
/api/tasks/?ordering=created_at
/api/tasks/?ordering=-created_at
/api/subtasks/?ordering=created_at
/api/subtasks/?ordering=-created_at
```

### Несколько параметров вместе

```text
/api/tasks/?status=New&search=presentation&ordering=-created_at
/api/subtasks/?status=Done&search=report&ordering=created_at
```

## Проверка CRUD через браузер или Postman

1. POST `/api/tasks/` — создать задачу.
2. GET `/api/tasks/` — проверить список.
3. GET `/api/tasks/1/` — получить задачу по ID.
4. PATCH `/api/tasks/1/` — изменить одно или несколько полей.
5. DELETE `/api/tasks/1/` — удалить задачу.

Аналогично проверьте операции для `/api/subtasks/`.

Пример JSON для создания задачи:

```json
{
    "title": "Prepare final presentation",
    "description": "Prepare materials and slides.",
    "status": "New",
    "deadline": "2026-12-20T18:00:00Z"
}
```


Новые миграции не нужны, потому что модели не изменялись.
