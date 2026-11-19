# Homework 19 — продолжение Task Manager (ДЗ 8–18)

Этот проект продолжает без замены исходный Task Manager из Homework 18.
Сохранены задачи, подзадачи, категории, фильтрация, статистика, мягкое удаление категорий,
пагинация, логирование и JWT. Добавлены владельцы Task/SubTask, фильтрация по владельцу,
проверка прав и Swagger.

## Запуск
```bash
python -m venv venv
# Windows PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Проверка
- JWT: `POST /api/token/`
- API задач: `/api/tasks/`
- API подзадач: `/api/subtasks/`
- Swagger: `/swagger/`
- ReDoc: `/redoc/`

После входа используйте `Authorization: Bearer <access>`.
Пользователь видит только свои задачи и подзадачи. Создание задачи автоматически записывает владельца.

## Автоматические тесты

```bash
python manage.py test
```
