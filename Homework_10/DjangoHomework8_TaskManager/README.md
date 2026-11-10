# Домашнее задание 10 — ORM запросы (Task Manager)

Проект продолжает ДЗ №8 и ДЗ №9. Модели и поля из предыдущих заданий сохранены.
В ДЗ №10 добавлена management-команда, которая выполняет все требуемые CRUD-запросы.

## Запуск

Откройте папку `DjangoHomework8_TaskManager` в PyCharm.

Активируйте виртуальное окружение и установите зависимости:

```bash
pip install -r requirements.txt
```

Примените миграции:

```bash
python manage.py migrate
```

## Выполнение ДЗ №10

В терминале PyCharm выполните:

```bash
python manage.py homework10
```

Команда последовательно:
1. Создаёт Task `Prepare presentation`.
2. Создаёт SubTask `Gather information` и `Create slides`.
3. Выводит задачи со статусом `New`.
4. Выводит просроченные подзадачи со статусом `Done`.
5. Меняет статус основной задачи на `In progress`.
6. Переносит дедлайн `Gather information` на два дня назад.
7. Меняет описание `Create slides`.
8. Удаляет основную задачу и проверяет, что подзадачи удалились вместе с ней.

Команду можно запускать повторно: перед созданием она удаляет прежнюю учебную
задачу с таким названием, если та осталась в базе.

## Код запросов

Полный код всех ORM-запросов находится здесь:

`tasks/management/commands/homework10.py`

Примеры основных запросов:

```python
# CREATE
task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation.",
    status="New",
    deadline=timezone.now() + timedelta(days=3),
)

# CREATE связанных подзадач
SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation.",
    status="New",
    deadline=timezone.now() + timedelta(days=2),
    task=task,
)

# READ
Task.objects.filter(status="New")
SubTask.objects.filter(status="Done", deadline__lt=timezone.now())

# UPDATE
Task.objects.filter(title="Prepare presentation").update(status="In progress")
SubTask.objects.filter(title="Gather information").update(
    deadline=timezone.now() - timedelta(days=2)
)
SubTask.objects.filter(title="Create slides").update(
    description="Create and format presentation slides."
)

# DELETE: подзадачи удалятся автоматически (CASCADE)
Task.objects.filter(title="Prepare presentation").delete()
```


## Важное пояснение к запросу Done

В задании новые подзадачи создаются со статусом `New`. Поэтому запрос на поиск
просроченных подзадач со статусом `Done` в момент чтения может вернуть пустой
результат. Это нормальное поведение фильтра, а не ошибка. Дальше по заданию
дедлайн `Gather information` переносится в прошлое, но его статус остаётся `New`.
