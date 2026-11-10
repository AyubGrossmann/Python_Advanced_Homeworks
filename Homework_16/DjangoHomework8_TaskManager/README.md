# Домашнее задание 16 — Category ModelViewSet и мягкое удаление

Проект продолжает Task Manager из ДЗ №8–15. Предыдущие модели, API и Generic Views
сохранены. Для категории добавлены полный CRUD через ModelViewSet, action для
подсчёта задач и мягкое удаление.

## Что реализовано

### Задание 1. CategoryViewSet

В `tasks/views.py` создан класс `CategoryViewSet`, который наследуется от
`ModelViewSet`. Он поддерживает:

- GET `/api/categories/` — список активных категорий;
- POST `/api/categories/` — создание категории;
- GET `/api/categories/1/` — получение категории;
- PUT/PATCH `/api/categories/1/` — обновление категории;
- DELETE `/api/categories/1/` — мягкое удаление категории.

Для маршрутов используется `DefaultRouter`.

### Кастомный action count_tasks

GET `/api/categories/1/count_tasks/`

Возвращает ID категории, её название и количество связанных задач.

### Задание 2. Мягкое удаление

В модель Category добавлены поля:

- `is_deleted` — BooleanField, по умолчанию False;
- `deleted_at` — DateTimeField, допускает NULL.

Метод `delete()` не удаляет строку из базы, а устанавливает `is_deleted=True`
и записывает дату и время удаления.

`ActiveCategoryManager.get_queryset()` по умолчанию показывает только
категории, у которых `is_deleted=False`.

Дополнительно есть `Category.all_objects`, который позволяет получить все
категории, в том числе удалённые.

## Установка и запуск

Откройте папку `DjangoHomework8_TaskManager` в PyCharm.

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

В этом задании появилась новая миграция `0003_category_soft_delete.py`.
Команда `migrate` применит её автоматически.

## Проверка API

### 1. Получить список категорий

GET:

`http://127.0.0.1:8000/api/categories/`

### 2. Создать категорию

POST:

`http://127.0.0.1:8000/api/categories/`

JSON:

```json
{
    "name": "Work"
}
```

### 3. Посчитать задачи категории

GET:

`http://127.0.0.1:8000/api/categories/1/count_tasks/`

Пример ответа:

```json
{
    "category_id": 1,
    "category_name": "Work",
    "tasks_count": 3
}
```

Число зависит от реальных связанных задач.

### 4. Обновить категорию

PATCH:

`http://127.0.0.1:8000/api/categories/1/`

JSON:

```json
{
    "name": "Study"
}
```

### 5. Мягко удалить категорию

DELETE:

`http://127.0.0.1:8000/api/categories/1/`

После удаления категория исчезнет из обычного списка, но останется в базе
с `is_deleted=True` и заполненным `deleted_at`.

Проверить удалённые категории можно через Django shell:

```bash
python manage.py shell
```

```python
from tasks.models import Category

# Только активные категории:
Category.objects.all()

# Все категории, включая удалённые:
Category.all_objects.all()

# Посмотреть удалённые:
Category.all_objects.filter(is_deleted=True)
```

## Важное замечание

Поле `name` в модели остаётся уникальным на уровне базы данных. Поэтому название
уже удалённой категории нельзя повторно использовать. Это помогает избежать
конфликта с уникальным ограничением.

Мягкое удаление применяется при удалении категории через API (ModelViewSet
вызывает метод `delete()` объекта). Массовый `QuerySet.delete()` для мягкого
удаления не используется.

