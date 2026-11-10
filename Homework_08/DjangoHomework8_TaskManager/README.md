# Homework 8 — Task Manager (Django)

Учебный проект для домашнего задания: модели Task, SubTask и Category,
регистрация моделей в Django Admin и добавление тестовых объектов.

## 1. Установка

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

Установить Django:
```bash
pip install -r requirements.txt
```

## 2. Миграции и запуск

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте:
- Сайт: http://127.0.0.1:8000/
- Админка: http://127.0.0.1:8000/admin/

Войдите в админку с данными суперпользователя и создайте несколько Category,
Task и SubTask. В Task можно выбрать несколько категорий и назначить дедлайн.

## Структура

- `tasks/models.py` — три модели задания.
- `tasks/admin.py` — регистрация и настройки отображения в админке.
- `tasks/migrations/0001_initial.py` — начальная миграция.
- SQLite используется по умолчанию, поэтому отдельная база данных не нужна.


