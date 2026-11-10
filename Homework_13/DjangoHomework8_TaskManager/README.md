# Домашнее задание 13 — Task Manager API

Проект продолжает предыдущие ДЗ №8–12. Существующие модели Task, SubTask и
Category сохранены. Добавлены сериализаторы и API-представления для подзадач.

## Что реализовано

### Задание 1. SubTaskCreateSerializer

В `tasks/serializers.py` создан `SubTaskCreateSerializer`.
Поле `created_at` доступно только для чтения (`read_only=True`).

### Задание 2. CategoryCreateSerializer

Создан сериализатор категории:
- при создании проверяется уникальность `name`;
- при обновлении проверяется, нет ли другой категории с таким именем;
- если название уже занято, возвращается ошибка валидации.

### Задание 3. Вложенный TaskDetailSerializer

`TaskDetailSerializer` включает:

```python
subtasks = SubTaskSerializer(many=True, read_only=True)
```

Благодаря `related_name="subtasks"` API показывает все подзадачи конкретной задачи.

### Задание 4. TaskCreateSerializer

Метод `validate_deadline` запрещает устанавливать дедлайн в прошлом.

### Задание 5. Представления для SubTask

Используются APIView-классы на основе generic views:
- `SubTaskListCreateView` — список и создание;
- `SubTaskRetrieveUpdateDestroyView` — получение, изменение и удаление.

## Установка и запуск

Откройте папку `DjangoHomework8_TaskManager` в PyCharm.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Базовый адрес API: `http://127.0.0.1:8000/api/`

## Endpoints

| Метод | URL | Назначение |
|---|---|---|
| GET | `/api/tasks/` | Список задач |
| POST | `/api/tasks/` | Создание задачи |
| GET | `/api/tasks/1/` | Задача по ID вместе с подзадачами |
| GET | `/api/tasks/statistics/` | Статистика задач |
| GET | `/api/subtasks/` | Список подзадач |
| POST | `/api/subtasks/` | Создание подзадачи |
| GET | `/api/subtasks/1/` | Получение подзадачи |
| PUT/PATCH | `/api/subtasks/1/` | Обновление подзадачи |
| DELETE | `/api/subtasks/1/` | Удаление подзадачи |

Замените `1` на ID существующей записи.

## Примеры запросов

### Создать подзадачу

POST `/api/subtasks/`

```json
{
    "title": "Prepare documentation",
    "description": "Write API documentation.",
    "task": 1,
    "status": "New",
    "deadline": "2026-12-20T18:00:00Z"
}
```

`created_at` отправлять не нужно: сервер заполняет его автоматически.

### Проверить вложенные подзадачи

GET `/api/tasks/1/`

В ответе у задачи будет поле `subtasks` со списком связанных подзадач.

### Проверить валидацию дедлайна

POST `/api/tasks/`

```json
{
    "title": "Test old deadline",
    "description": "Check deadline validation.",
    "status": "New",
    "deadline": "2020-01-01T10:00:00Z"
}
```

Ожидаемый результат — ошибка валидации, потому что дата находится в прошлом.

### Проверить уникальность категории

POST `/api/categories/` не входит в маршруты этого задания, поскольку в условии
требуется определить CategoryCreateSerializer, но не требуется создавать
отдельный endpoint для категорий. Сериализатор можно проверить в Django shell
или подключить отдельный view при необходимости.

Для этого задания структура моделей не менялась, поэтому новые миграции не нужны.
