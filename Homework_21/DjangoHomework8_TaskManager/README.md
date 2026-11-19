# Homework 21 — Signals и Email в Task Manager

Это следующая версия того же проекта из Homework 20, который продолжает Homework 19 и 8–18.
Сохранены все предыдущие API, владельцы, permissions, Swagger, регистрация и JWT cookies.
Добавлен Django Signal: владелец главной задачи получает email при реальном изменении статуса.
Повторное сохранение без изменения статуса письмо не отправляет.

## Запуск
```bash
python -m venv venv
# Windows PowerShell: venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Email backend учебный: письмо выводится в терминал Django. Это соответствует заданию
использовать базовый тестовый сервер и выводить шаблон сообщения в консоль.

## Endpoints
Все endpoints из Homework 19 и 20 сохранены. Swagger: `/swagger/`.
Для отправки уведомления создайте задачу от имени пользователя с email, затем измените
её статус через API или Django Admin. Сообщение появится в консоли.

## Автоматические тесты

```bash
python manage.py test
```
